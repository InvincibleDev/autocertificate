from certificate.apis.viewsets import *
from rest_framework import routers

router= routers.DefaultRouter()
router.register('certificates', CertificateViewSet, base_name='certificate_base')
router.register('csv', CsvViewset, base_name='csv')
router.register('template', TemplateViewset, base_name='template')
router.register('signup', SignupViewset)
router.register('blankupload',BlankViewset,base_name='blankupload')
