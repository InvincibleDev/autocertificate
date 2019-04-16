from certificate.models import *
from .serializer import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.parsers import FormParser, MultiPartParser
import xlrd
import os
from PIL import Image , ImageDraw , ImageFont


# class CertificateViewSet(viewsets.ModelViewSet):
#     serializer_class=TemplateSerializer
#
#     def get_queryset(self):
#         pk = self.request.data['pk']
#         user = User.objects.get(pk=pk)
#         queryset = Templates.objects.filter(user=user)
#         return queryset


class SignupViewset(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=(AllowAny,)


class BlankViewset(viewsets.ViewSet):
    def create(self,request):
        template_id=request.data.get('template_id')
        template=Templates.objects.get(id=template_id)
        blanks=request.data.get('blanks')
        user=request.user
        header_list={}
        for blank in blanks:
            blankobj=Blanks.objects.create(templates=template,blank_no=blank['blank_no'],start=blank['start'],end=blank['end'])
            header_list[blank['blank_no']] = blank['col_name']
        try:
            csvfile=Csv.objects.get(csvfile=f"userfiles/{request.user.username}.xlsx")
        except:
            return Response({'detail':'CSVFileDoesNotExist'})
        link=self.makecertificates(template,csvfile,header_list)
        return Response({'link':link})


    def makecertificates(self,template,csvfileobj,header_list):
        # wb = xlrd.open_workbook(file_contents=csvfileobj.csvfile.read())
        # sheet = wb.sheet_by_index(0)
        # headers=sheet.row(0)
        # for header in header_list:
        #     blanks=Blanks.objects.filter(templates=template,blank_no=header['blank_no'])
        pass


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
        if not csvfile.name.endswith(".xlsx"):
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
        serializer=CsvSerializer({"headers":[i.value for i in headers]})
        return Response(serializer.data)


    def get_headers(self,csvfile):
        wb = xlrd.open_workbook(file_contents=csvfile)
        sheet = wb.sheet_by_index(0)
        headers=sheet.row(0)
        return headers



class TemplateViewset(viewsets.ViewSet):
    def create(self,request):
        templatefile=request.FILES.get('template',None)
        if not templatefile:
            return Response({"detail":"FileNotFount"})
        if not templatefile.name.endswith(".jpg") or templatefile.name.endswith(".png") or templatefile.name.endswith(".jpeg"):
            return Response({"detail":"UnSupportedFileFormat"})
        Templateobejct=Templates.objects.create(template=templatefile,user=request.user)
        return Response({"detail":"TemplateUploadedSucessfully"})
