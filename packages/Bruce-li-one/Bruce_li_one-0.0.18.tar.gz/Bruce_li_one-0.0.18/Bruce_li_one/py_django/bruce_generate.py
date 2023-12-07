
import os
class Bruce_generate:
    def make_migrate_bat(self):
        """
        生成django项目windows的迁移文件
        """
        data="python manage.py makemigrations  && python manage.py migrate"
        file_name="migrate.bat"
        file_path=os.path.dirname(os.path.abspath(__file__))
        with open(file_path+file_name, 'w') as file:
            file.write(data)
    def make_migrate_sh(self):
        """
        生成django项目liunx的迁移文件
        """
        data = "python manage.py makemigrations  && python manage.py migrate"
        file_name = "migrate.sh"
        pass
    def make_run_bat(self,port=8000):
        """
        生成django项目windows的bat运行文件
        """
        data="python manage.py runserver 0.0.0.0:8000"
        file_name = "run.bat"
        pass
    def make_run_sh(self,port=8000):
        """
        生成django项目liunx的sh运行文件
        """
        data="python manage.py runserver 0.0.0.0:8000"
        file_name = "run.sh"
        pass