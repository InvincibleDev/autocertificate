from certificate.models import *
from .serializer import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.parsers import FormParser, MultiPartParser
import xlrd
import os
from PIL import Image , ImageDraw , ImageFont
from ast import literal_eval
from django.http import HttpResponse
from io import StringIO,BytesIO
import base64
from autocertificate import settings
import boto3
import botocore
import shutil




# class CertificateViewSet(viewsets.ModelViewSet):
#     serializer_class=TemplateSerializer
#
#     def get_queryset(self):
#         pk = self.request.data['pk']
#         user = User.objects.get(pk=pk)
#         queryset = Templates.objects.filter(user=user)
#         return queryset


class SignupViewset(viewsets.ViewSet):
    permission_classes=(AllowAny,)

    def create(self , request):
        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    )
            return Response({'detail':user.id})
        except:
            return Response({'detail':'unable to create user'})

    def list(self,request):
        queryset= User.objects.all()
        serializer=UserSerializer(queryset,many=True)
        return Response(serializer.data)

    def retrieve(self,request,pk=None):
        queryset= User.objects.filter(pk=pk)
        serializer=UserSerializer(queryset,many=True)
        return Response(serializer.data)


class BlankViewset(viewsets.ViewSet):
    def create(self,request):
        template_id=request.data.get('template_id')
        template=Templates.objects.get(id=template_id)
        blanks=request.data.get('blanks')
        user=request.user
        header_list={}
        for blank in blanks:
            try:
                blankobj=Blanks.objects.create(templates=template,blank_no=blank['blank_no'],start=blank['start'],end=blank['end'])
                header_list[blank['blank_no']] = blank['col_name']
            except Exception as e:
                return Response({'detail':str(e)})
        try:
            csvfile=Csv.objects.get(csvfile=f"userfiles/{request.user.username}.xlsx")
        except:
            return Response({'detail':'CSVFileDoesNotExist'})
        link=self.makecertificates(template,csvfile,header_list,blanks,request)
        return Response({'link':link})


    def makecertificates(self,template,csvfileobj,header_list,blanks,request):
        wb = xlrd.open_workbook(file_contents=csvfileobj.csvfile.read())
        sheet = wb.sheet_by_index(0)
        headers=sheet.row(0)
        in_memory = StringIO()
        buffered = BytesIO()
        os.mkdir(f'{request.user.username}')
        path=str(settings.BASE_DIR)+(f'\{request.user.username}')
        font = ImageFont.truetype("arial.ttf", 20)


        #connecting to s3
        s3 = boto3.resource('s3',aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY)

        bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        exists = True
        try:
            s3.meta.client.head_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        except botocore.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                exists = False
        #

        for blank in blanks:
            start=literal_eval(blank['start'])
            end=literal_eval(blank['end'])
            for i in range(sheet.ncols):
                if sheet.cell_value(0, i) == blank['col_name']:
                    blank['values']=sheet.col_values(i)
                    blank['start']=start
                    blank['end']=end
        for i in range(sheet.nrows):
            img=Image.open(template.template)
            imgdraw=ImageDraw.Draw(img)

            for blan in blanks:
                imgdraw.text(blan['start'],blan['values'][i],font=font,fill=(255,0,0,255))
            img.save(f'{request.user.username}/{request.user.username}{i}certificate.pdf',"PDF",resoultion = 100.0)

        shutil.make_archive(f'{template.title}', 'zip', path)
        zipdata = open(os.path.join(settings.BASE_DIR, f'{template.title}.zip'), 'rb').read()
        s3.Object(settings.AWS_STORAGE_BUCKET_NAME,f'zips/{request.user.username}/{template.title}.zip').put(Body=zipdata,ACL='public-read')
        link=f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/zips/{request.user.username}/{template.title}.zip'
        link_=Link.objects.create(user=request.user,link=link,template_title=template.title)

        shutil.rmtree(path)
        os.remove(os.path.join(settings.BASE_DIR, f'{template.title}.zip'))

        return link_.link


class LinkViewset(viewsets.ViewSet):

    def list(self,request):
        queryset= Link.objects.filter(user=request.user)
        serializer=LinkSerializer(queryset,many=True)
        return Response(serializer.data)

    def retrieve(self,request,pk=None):
        queryset= Link.objects.filter(pk=pk)
        serializer=LinkSerializer(queryset,many=True)
        return Response(serializer.data)


class CertificateViewSet(viewsets.ViewSet):

    def list(self,request):
        queryset= Templates.objects.filter(user=request.user)
        serializer=TemplateSerializer(queryset,many=True)
        return Response(serializer.data)

    def retrieve(self,request,pk=None):
        queryset= Templates.objects.filter(pk=pk)
        serializer=TemplateSerializer(queryset,many=True)
        return Response(serializer.data)

class CsvViewset(viewsets.ViewSet):
    def create(self,request):
        csvfile=request.FILES.get('csv',None)
        if not csvfile:
            return Response({"detail":"FileNotFount"})
        if not csvfile.name.endswith(".xlsx") or csvfile.name.endswith(".csv"):
            return Response({"detail":"UnSupportedFileFormat"})
        try:
            existingfile=Csv.objects.filter(csvfile=f"userfiles/{request.user.username}.xlsx")
            for file in existingfile:
                file.csvfile.delete()
                file.delete()
        except Exception as e:
            print("doesnt exits")
        csvfile.name=f"{request.user.username}.xlsx"
        csvobject=Csv.objects.create(csvfile=csvfile)
        headers=self.get_headers(csvobject.csvfile.read())
        if not headers:
            return Response({"detail":"Unable to open file, File corrupted. Upload a new file"})
        serializer=CsvSerializer({"headers":[i.value for i in headers]})
        return Response(serializer.data)


    def get_headers(self,csvfile):
        try:
            wb = xlrd.open_workbook(file_contents=csvfile)
            sheet = wb.sheet_by_index(0)
            headers=sheet.row(0)
            return headers
        except Exception as e:
            return False



class TemplateViewset(viewsets.ViewSet):
    def create(self,request):
        templatefile=request.FILES.get('template',None)
        title=request.data.get('title')
        if not templatefile:
            return Response({"detail":"FileNotFount"})
        if not (templatefile.name.endswith(".jpg") or templatefile.name.endswith(".png") or templatefile.name.endswith(".jpeg")):
            return Response({"detail":"UnSupportedFileFormat"})
        Templateobejct=Templates.objects.create(template=templatefile,user=request.user,title=title)
        return Response({"detail":"TemplateUploadedSucessfully"})
