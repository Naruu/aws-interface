<div align="center">
  <img src="https://s3.ap-northeast-2.amazonaws.com/aws-interface.com/assets/img/brand/blue.png"><br><br>
</div>



![Language](https://img.shields.io/badge/Language-Python3.6-blue.svg)
![Language](https://img.shields.io/badge/NaverFest-Finalist-brightgreen.svg)
[![Build Status](https://travis-ci.org/hubaimaster/aws-interface.svg?branch=master)](https://travis-ci.org/hubaimaster/aws-interface)

**[Naver D2 Fest 결승 우수상 수상!!](https://github.com/D2CampusFest/6th)**
## Globalization
- **[English](https://github.com/hubaimaster/aws-interface/blob/master/README.md)**
- **[Korean (한국어)](https://github.com/hubaimaster/aws-interface/blob/master/README_KR.md)**

# AWS-Interface

**AWS 인터페이스** (이하 AWSI) 는 Amazon Web Services (AWS)에서 제공하는 IAM, DynamoDB, Lambda, API Gateway 등의 서비스를 추상화하여 손쉽게 사용할 수 있게 해주는 인터페이스입니다.

새로운 서비스를 제작할 때, 주로 확장성과 초기 투자 비용 사이의 trade-off를 고민하게 됩니다. 처음에는 EC2 인스턴스를 하나 파서 웹 프레임워크와 함께 서버 안에서 돌려도 되지만, 서비스가 커지면 AWS DynamoDB와 같은 서비스를 고려해야 합니다. 사실 DynamoDB도 확장성 좋고 쓰기 쉬운 서비스라고 만들었겠지만, 정작 능숙하게 다룰줄 아는 개발자가 몇명이나 될까요?

AWS 인터페이스는 이런 문제를 해결하기 위해서 추상적인 개념만으로 서비스를 구성할 수 있도록 합니다. AWSI 에서 어플리케이션을 생성하면 실제 백엔드를 담당하는 AWS 등의 IaaS 서비스가 자동으로 구성되고 이와 손쉽게 통신할 수 있는 플랫폼별 SDK가 만들어집니다. 서비스를 관리할 수 있는 대시보드 또한 AWS 인터페이스에서 제공됩니다.

## 서비스 구성 (사용자 입장)

### Service (서비스)
서비스하고자 하는 앱의 백엔드 및 DB 단에 들어갈 요소를 설정하는 단위입니다. 서비스에 추가할 추상화된 기능이라고 생각할 수 있습니다. 초기에는 6가지 Service 를 지원할 예정입니다.

- Bill: 백엔드 요금 사용 내역 확인
- Auth: 로그인 및 사용자 인증
- Database: 각종 데이터
- Storage: 파일 저장 및 배포
- Logic : 서버리스 API 코드 생성 및 배포
- Log : 사용자 로그 기록 및 확인

### Dashboard (대시보드)
레시피를 구성하고, DB를 관리할 수 있는 웹 인터페이스를 대시보드라고 부릅니다. [aws-interface.com](http://aws-interface.com) 에서  IAM 정보를 입력해서 계정을 만들거나 로컬에서 호스팅된 대시보드에 IAM 정보를 등록한 후에 이용 가능합니다. 웹 인터페이스는 Django 프레임워크를 기반으로 합니다.

### Backend (백엔드)
실제 뒷단에서 사용하는 IaaS 서비스를 말합니다. 현재는 AWS 백엔드만 제공하지만 향후에는 Google Cloud Platform, Naver Cloud Platform, 테스트용 Local Deployment 등을 추가적으로 지원할 예정입니다.

### Client SDK
레시피를 기반으로 자동으로 구성된 백엔드를 클라이언트 앱에서 접근하기 위한 SDK를 말합니다. SDK는 Python, Swift, Java 등 다양한 플랫폼에서 지원하는 언어로 자동 생성됩니다.

## 서비스 설계 (개발자 입장)
<div align="center">
  <img src="https://s3.ap-northeast-2.amazonaws.com/aws-interface.com/docs/awsist.png"><br><br>
</div>

### Django
장고 웹 인터페이스 단에서는 위의 core 클래스들을 import 해서 필요한 함수를 Adapter 를 통해 호출하는 방식으로 구현됩니다.

### Adapter Abstract Class
사용자의 Credential 과 app_id 를 생성자 파라메터로 받아와 API 와 ResourceAllocator 를 함께 묶어서 상위 레이어에서 기능을 손쉽게 사용할 수 있도록 해줍니다. 예를들어 상위 레이어가 Django 라면 Adapter 를 상속한 
DjangoAdapter 만들어서 사용합니다. 

### ServiceController Abstract Class 
Cloud 레이어에서 구현된 기능을 AWS 나 Azure 를 거치지 않고 직접 호출할 수 있게 해주는 Wrapping 레이어입니다.

### Cloud Module
Auth, Database 등의 기능을 Resource 를 호출하여 구현합니다. 이 모듈은 ServiceController 에 의해 호출되며, 동시에 ResourceAllocator 에 의해
AWS Lambda 같은 Server-less 아키텍쳐에 업로드됩니다. 

### Resource Abstract Class
이 레이어 덕분에 AWS 를 포함해 Azure, GCP, NCP 등의 Cloud Service 를 사용할 수 있습니다.
예를 들어 Resource 를 상속한 AWSResource 를 구현하면 사용자는 Backend 로 AWS 를 사용할 수 있습니다.

### ResourceAllocator Abstract Class
Resource 레이어에서 사용할 Cloud service 의 상태를 초기화 합니다. DB 인스턴스를 생성하거나 Server-less function 서비스에 
Cloud 모듈을 업로드하는 등의 작업을 통해 Resource 를 사용할 수 있게 준비하는 역할을 합니다. 예를 들어 AWSResourceAllocator 는 AWS 에서 boto3 모듈을 통해 DynamoDB, 
Lambda, API Gateway 등을 생성하여 Resource 를 사용할 수 있게 준비합니다.

### SDK
ResourceAllocator 의 Superclass 에 의해 자동으로 생성되는 SDK 입니다. 해당 SDK 를 클라이언트에 Import 하여 다양한 플랫폼에서 
Service 에 접근할 수 있습니다.

### AWS 상세 구현
대시보드에서 어플리케이션을 생성하면 AWS 내의 DynamoDB 테이블과 Lambda 함수 그리고 API Gateway 가 자동으로 Lambda 에 연결됩니다. 이어 자동으로 생성된 SDK 는 API Gateway와 http 방식으로 통신을 하게 됩니다.

예를 들어, 아래는 Auth Service 가 실제 작동하는 과정입니다.

1. (사용자) AWS IAM 인증 정보를 AWS 인터페이스에 등록하여 가입합니다.
2. (사용자) 대시보드에서 어플리케이션을 생성하고 서비스 구성을 변경합니다.
3. (AWS 인터페이스) DynamoDB에서 단일 테이블을 만들고 그 안에 사용자 모델을 생성합니다. 
4. (AWS 인터페이스) 모델들을 읽고 쓸 수 있는 Lambda 함수를 작성합니다.
5. (AWS 인터페이스) 작성된 Lambda 함수를 외부에서 이용할 수 있게 API Gateway 와 연결합니다.
6. (AWS 인터페이스) API Gateway 에 외부에서 접근할 수 있는 SDK를 Java, Python, Swift 등으로 자동 생성합니다.
7. (사용자) 자동 생성된 SDK를 클라이언트 앱에서 불러와서 AWS 리소스와 통신합니다.

## 환경 설정

### Python 버젼 및 라이브러리

AWS 인터페이스는 Python 3.6에서 작성되었습니다. 

Python 모듈 설치는 프로젝트 단위로 독립적으로 하시면 좋아요! 요런걸 주로 virtual environment라고 부르는데, 방법은 정말 [다양](https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe)합니다.

아래는 Python 3에서 제공하는 공식 패키지인 venv를 사용하는 방식입니다.

```bash
# Ubuntu 등에서 Python 설치
sudo apt update
sudo apt install python3
sudo apt install python3-venv
```

```
python3 -m venv venv
source venv/bin/activate  # virtual environment 작동
pip install -r requirements.txt  # 패키지 설치
# deactivate 이거는 virtual environment 해제
```

#### AWS EC2 (Ubuntu) 사용자를 위한 Python 버전 팁
Ubuntu 16.04에서 apt로 받을 수 있는 기본 Python3 버전은 3.5입니다. 다른 방식으로 Python 버전을 올릴 수는 있지만, 처음부터 EC2 인스턴스를 Ubuntu 18.04로 만드는 것을 추천드립니다.

### IAM 계정
AWS 인터페이스를 이용하기 위해서는 AWS 계정에 접속할 수 있는 관리자 권한이 필요합니다. 대시보드에 접근하기 위해서는 AWS 계정 내에서 관리자 권한을 가진 IAM User의 Access Key와 Secret Access Key를 입력해야 합니다.

#### 참고
- [AWS 계정 생성](https://aws.amazon.com/ko/premiumsupport/knowledge-center/create-and-activate-aws-account/)
- [IAM 계정 생성](https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/id_users_create.html)

## 빠른 실행
다음 명령어를 이용해서 로컬 대시보드 서버를 호스팅하여 테스트해보실 수 있습니다.
```
# activate virtual environment
cd aws_interface
python3 manage.py migrate --run-syncdb
python3 manage.py runserver
# open 127.0.0.1:8000 on your browser
```

## Contribution 가이드라인

버그 리포팅과 피드백을 받기 위해 [깃허브 이슈](https://github.com/hubaimaster/AWSInterface/issues)를 사용하고 있습니다.

- 클라이언트 SDK 자동 생성 언어 확장 관련 Contribution 환영합니다.
- AWSInterface 프로젝트는 Apache 2.0 라이센스를 따릅니다.

### Git Commit 메시지
Commit 메시지는 [다음과 같은 형식](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)으로 해주세요. Reddit 유저 왈, "the defacto standard".

```
Capitalized, short (50 chars or less) summary

More detailed explanatory text, if necessary.  Wrap it to about 72
characters or so.  In some contexts, the first line is treated as the
subject of an email and the rest of the text as the body.  The blank
line separating the summary from the body is critical (unless you omit
the body entirely); tools like rebase can get confused if you run the
two together.

Write your commit message in the imperative: "Fix bug" and not "Fixed bug"
or "Fixes bug."  This convention matches up with commit messages generated
by commands like git merge and git revert.

Further paragraphs come after blank lines.

- Bullet points are okay, too

- Typically a hyphen or asterisk is used for the bullet, followed by a
  single space, with blank lines in between, but conventions vary here

- Use a hanging indent
```

#### 사용된 오픈소스 프로젝트

- [django](https://github.com/django/django)
- [argon-design-system](https://github.com/creativetimofficial/argon-design-system)

