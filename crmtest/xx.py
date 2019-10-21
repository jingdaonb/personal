import  os
import random



if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crmtest.settings")
    import  django
    django.setup()
    from app01 import  models

    l=[]
    for i  in  range(1,101):
        obj=models.Customer(
            qq=random.randint(10000000000,99999999999),
            name='大白'+str(i),
            sex=random.choice(['male','demale']),
            source=random.choice(['qq','website']),
            course=random.choice(['LinuxL','PythonFullStack'])
        )
        l.append(obj)

    models.Customer.objects.bulk_create(l)