import setuptools
'''
1. Python 홈페이지 의 pyPi 클릭 
레지스트리 - 회원가입 - 로그인 

- python_package
    - sean_pack
        - __init_.py
        - func.py
        - func1.py
        - ...
    - another folder
        - ..py
        - ..py

    setup.py    ## 최고 상위 폴더 아래 만들어주어야함. 
    
    
위와같은 구조로 정리.후    

build하기 위한 패키지 설치
pip install setuptools wheel

setup.py 파일을 만들고  (주의 name 에 _ 는 들어가지 않음)
README.txt 파일을 __init__.py 와 동상 위치에 만든다 아무거나. 
setup.py 파일이 있는 폴더(최상위폴더 아래)로 터미널로 이동
> python setup.py sdist bdist_wheel 
실행 

dist 폴더안에 업로드할 파일이 생김. 

## 업로드 하는 패키지 설치 
pip install twine

## 업로드하기
python -m twine upload dist/*
pipy id 입력
password 입력

## 만약 기존 업로드 된것의 버전변경이 없는경우 업로드 되지 않음. 버전을 바꿔주어야함. 
'''

setuptools.setup(
    name = 'bigpi' ,  ## package index id ? 폴더명과 관계없이 이 이름으로 패키지가 설치된다. ** 그냥 폴더명따르는것 같음. 걍 폴더명과 같이 쓰자.
    version='0.0.2', 
    author='Sean Lee', 
    author_email='twmllsh@gmail.com',
    description='this is my test package',
    long_description='when I young, ..........',
    long_description_content_type='text/markdown', 
    url='https://github.com/twmllsh',
    packages=setuptools.find_packages(),   ### 폴더안에 들어있는 패키지들을 찾아서 설치하게 만든다.
    # include_package_data=True, ## 패키지 안에 data도 포함시킨다
    # zip_safe = False   ## 압축이냐 아니냐.. 아마 pypi 에 올릴때는 압축해야하는거 같음. 
    # install_requires= [                       ## "numpy < 1.15" 이렇게 하면 버전제한 할수 있다.
    #     "numpy",
    # ]
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7'
    
)