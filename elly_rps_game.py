# 제작자 : hayden90

import random as r
import time
import os
import json
import hashlib
import getpass
import random

ment_list = [
  "도박은 순간의 쾌락, 결과는 평생의 후회입니다.",
  "도박에서 얻은 돈은 행복을 가져다주지 않습니다. 당신의 노력만이 행복을 가져다 줍니다.",
  "승리의 꿈은 짧고, 도박의 덫은 깊습니다.",
  "한 번의 도박으로 잃을 수 있는 것은 돈만이 아닙니다. 당신의 삶을 소중히 여기세요.",
  "도박은 문제를 해결하지 않습니다. 오히려 새로운 문제를 만들 뿐입니다.",
  "도박에 빠지는 순간, 당신의 삶은 통제 불능이 됩니다. 스스로를 지키셔야 합니다.",
  "건강한 삶을 위한 첫 걸음은 도박을 멀리하는 것입니다.",
  "도박의 유혹을 뿌리치고, 더 나은 내일을 위해 투자하세요.",
  "도박에서 벗어나는 용기가 당신을 자유롭게 합니다.",
  "도박을 멈추는 것은 새로운 인생의 첫걸음입니다."
]
random_ment = random.choice(ment_list)

# 실행하는 os가 리눅스면 'clear'명령어를, 윈도우면 'cls'를 입력하는 함수
def clearConsole():
  command = 'clear'
  if os.name in ('nt', 'dos'):
    command = 'cls'
  os.system(command)

clearConsole()

# 비밀번호를 해시하는 함수
def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 메인 메뉴 함수 생성
def main():
  while True:
    print(" 1. 로그인\n 2. 계정생성\n 3. 종료")
    main_input = input("숫자 입력 : ")
    if main_input in ['1', '로그인']: 
      login()
    elif main_input in ['2', '계정생성']: 
      user_create()
    elif main_input in ['3', '종료']: 
      exit()
    else:
      print('\033[38;2;220;30;0m' + "잘못된 입력입니다. 숫자 또는 한글을 입력해주세요."+ '\033[0m')

# 로그인 메뉴 함수 생성
def login():
  pass_time = 0
  max_attempts = 5
  while pass_time < max_attempts:
    print("로그인할 닉네임과 비밀번호를 입력하세요.")
    log_id_input = input("닉네임 : ")
    log_pass_input = getpass.getpass("비밀번호 : ")
    userInfo, exists = loadUser(log_id_input)
    if exists and userInfo["pass"] == hash_pass(log_pass_input):
      print("로그인 성공!")
      start_game(userInfo)
    else:
      pass_time += 1
      remaining_attempts = max_attempts - pass_time
      print('\033[38;2;220;30;0m' + f"로그인 실패. 닉네임 또는 비밀번호를 확인하세요. 남은 시도 횟수: {remaining_attempts}" + '\033[0m')
      if pass_time >= max_attempts:
        print("로그인 시도 횟수를 초과했습니다. 프로그램을 종료합니다.")
        exit()

# 새로운 사용자 가입하는 함수 생성
def user_create():
  print("생성할 닉네임과 비밀번호(4자리 이상)를 입력해주세요.")
  user_name = input("닉네임 : ")
  user_pass = getpass.getpass("비밀번호 입력 : ")
  user_pass_confirm = getpass.getpass("비밀번호 확인 : ")
  if len(user_pass) < 4:
    print('\033[38;2;220;30;0m' + "비밀번호는 4자리 이상이어야 합니다." + '\033[0m')
    return
  
  if user_pass != user_pass_confirm:
    print('\033[38;2;220;30;0m' + "두번 입력하신 비밀번호가 서로 일치하지 않습니다. 다시 시도해주세요." + '\033[0m')
    return

  userInfo, exists = loadUser(user_name)

  if exists:
    print('\033[38;2;220;30;0m' + "이미 존재하는 닉네임입니다. 다른 닉네임을 사용하세요." + '\033[0m')
  else:
    createUser(user_name, hash_pass(user_pass))
    print(f"{user_name}님, " + '\033[38;2;20;170;0m' + "회원가입이 완료" + '\033[0m' + "되었습니다. 로그인해주세요~")


# 새로운 사용자 추가하는 함수 생성
def createUser(user_name, user_pass):
  userList = load_users()
  user_coin = 1000  # 초기 코인 설정
  user_life = 2 # 계정 초기 생명 설정
  newUser = {"name": user_name, "pass": user_pass, "coin": user_coin, "life": user_life}
  userList.append(newUser)
  save_users(userList)
  return newUser, True

# 사용자 데이터에 따른 설정
def loadUser(user_name):
  userList = load_users()
  for user in userList:  
    if user["name"] == user_name:
      # 코인이 0일 경우 500코인 지급, 생명 -1
      if user["coin"] == 0:
        # 생명이 0일 경우 입장 거절
        if user["life"] <= 0:
          print(f"{user_name}님은" + '\033[38;2;220;30;0m' + " 전재산을 탕진하여 입장할 수 없습니다."+ '\033[0m')
          print(f"{user_name} : '주머니에 단돈 천원도 없네... 내 20년간 모은 재산이 하루만에 날아가다니...'")
          print('\033[38;2;255;150;0m' + random_ment + '\033[0m')
          time.sleep(2)
          exit()
        else : 
          clearConsole()
          print(f"{user_name} : 나는 방금 모든걸 잃었다... ")
          time.sleep(3)
          print(f"곤희 : 이봐! {user_name}님. 뽀찌받아 가야지. ")
          time.sleep(3)
          print('\033[38;2;20;170;0m' + "500코인이 지급되었습니다." + '\033[0m')
          user["coin"] = 500
          save_users(userList)
          time.sleep(2)
          print("곤희 : 거, 도박하지 마세요. ")
          time.sleep(2)
          print("곤희 : 다음번에 여기 또 오시면 나한테 죽습니다.")
          time.sleep(2)
          print(f"{user_name} : 고맙습니다.")
          time.sleep(2)
          print(f"({user_name}님은 천만다행인듯이 약간의 미소를 짓는다)")
          time.sleep(2)
          print("(곤희가 돌아간다)")
          time.sleep(2)
          print(f"{user_name} : ... ")
          time.sleep(3)
          print("(하우스 안에서 승리자의 웃음소리가 들린다.)")
          time.sleep(2)
          print("승리자 : 오~~예! 하하하")
          time.sleep(3)
          print("'그리고 나는 결심 한듯이 하우스장으로 다시 들어갔다...'")
          time.sleep(4)
          return user, True
      return user, True
  return None, False

# 사용자 정보를 저장하는 함수 생성
def save_users(userList):
  with open('users.txt', 'w', encoding='utf-8') as f:
    newUserList = json.dumps(userList, ensure_ascii=False)
    f.write(newUserList)

# 사용자 정보를 불러오는 함수 생성
def load_users():
  if not os.path.exists('users.txt'):
    return []
  try:
    with open('users.txt', 'r', encoding='utf-8') as f:
      fileData = f.read()
      if fileData:
        return json.loads(fileData)
      else:
        return []
  except (json.JSONDecodeError, IOError):
    print("사용자 데이터를 읽는 중 오류가 발생했습니다. 데이터를 초기화합니다.")
    return []

def game(com_num, user_num):
  if com_num == user_num:
    return "무승부"
  elif (com_num == 1 and user_num == 3) or (com_num == 2 and user_num == 1) or (com_num == 3 and user_num == 2):
    return "패배"
  else:
    return "승리"

def com_choice(com_num):
  if com_num == 1:
    return "가위"
  elif com_num == 2:
    return "바위"
  elif com_num == 3:
    return "보"

def user_choice_to_num(choice):
  if choice == "가위" or choice == '1':
    return 1
  elif choice == "바위" or choice == '2':
    return 2
  elif choice == "보" or choice == '3':
    return 3

def saveUser(userInfo, user_coin, user_life):
  userList = load_users()
  for user in userList:
    if user["name"] == userInfo["name"]:
      user["coin"] = user_coin
      user["life"] = user_life
      break
  save_users(userList)

def start_game(userInfo):
  user_name = userInfo['name']
  user_coin = userInfo['coin']
  user_life = userInfo['life']

  print(f"{user_name}님 가위, 바위, 보 게임에 오신 것을 환영합니다.")
  print("입장을 도와드리겠습니다. 잠시만 기다려주세요...\n")
  # 이유없이 1초간 기다리기
  for i in range(5):
    print(f"[Loading] 하우스 입장중{'.' * (i + 1)}", end="\r")
    time.sleep(1)

  clearConsole()
  print('\033[38;2;255;150;0m' + "[하우스 입장 완료]" + '\033[0m')
  time.sleep(2)
  clearConsole()

  if user_life >= 2:
    print(f"{user_name} : 나는 가난을 탈출하고자 10년간 모아둔 전재산을 가지고 하우스에 왔다.")
    time.sleep(3)
  else :
    print(f"{user_name} : 또 하우스에 오고 말았다.. 본전만 찾자.")
    time.sleep(3)

  print('\033[38;2;255;150;0m' + "카운터 : 안녕하세요~ 하우스에 오신걸 환영합니다~\n" + '\033[0m')
  time.sleep(2)

  if user_life >= 2:
    print("카운터 : 환전된 " + '\033[38;2;255;150;0m' + f"{user_coin:,}" + '\033[0m' + "코인이 지급되었습니다~\n카운터 : 자리는 저쪽이구요. 행운을 빕니다~\n")
    time.sleep(2)
    if user_name == "호구":
      print("엘리 : 안녕? 너가 오늘 내 상대야?")
      time.sleep(2)
      print("엘리 : 닉네임이... 호구?")
      time.sleep(2)
      print("엘리 : 아따 호구 왔는가~?..하하하하하")
      time.sleep(1)
      print("엘리 : 이번에도 안봐준다~")
    else:
      print("엘리 : 안녕? 처음보네~ 너가 오늘 내 상대야?")
      print("엘리 : 얼마 걸꺼야?")
  else:
    print(f"카운터 : 자리는 저쪽 입니다. 행운을 빕니다~\n")
    time.sleep(2)
    if user_name == "호구":
      print("엘리 : 아따 호구 또 왔는가~? 하하하하")
    else: 
      print("엘리 : 안녕? 또 보네~")
      print("엘리 : 얼마부터 시작할까??")

  while user_coin > 0:
    print('\033[38;2;255;150;0m' + f"\n남은 코인 : {user_coin:,}" + '\033[0m')

    while True:
      print("('종료' 입력 시 게임 종료)")
      bet_input = input("베팅할 금액 : ")
      if bet_input == "종료":
        saveUser(userInfo, user_coin, user_life)
        print("최종 코인: " + '\033[38;2;255;150;0m' + f"{user_coin:,}" + '\033[0m' + " 코인이 저장되었습니다.")
        time.sleep(2)
        print("게임을 종료합니다.")
        time.sleep(2)
        exit()
      try:
        bet_coin = int(bet_input)
        if bet_coin > user_coin:
          print('\033[38;2;220;30;0m' + "\n가지고 있는 코인보다 큽니다." + '\033[0m')
        else:
          break
      except ValueError:
        print('\033[38;2;220;30;0m' + "\n유효한 숫자를 입력해주세요." + '\033[0m')

    user_score = 0
    com_score = 0

    if bet_coin == user_coin:
      time.sleep(1)
      print(f"\n{user_name} : '하...올인이다...'")
      time.sleep(2)
      print(f"{user_name} : '싸늘하다. 가슴에 비수가 날아와 꽂힌다.'")
      time.sleep(2)
      print(f"{user_name} : '하지만 걱정하지마라. 너의 패턴은 파악됐으니까.'")
      time.sleep(2)

    while user_score < 2 and com_score < 2:
      user_input = input("\n1.가위, 2.바위, 3.보 중 하나를 입력하세요(숫자 또는 한글): ")

      if user_input not in ['가위', '바위', '보', '1', '2', '3']:
        print('\033[38;2;220;30;0m' + "\n잘못된 입력입니다. 다시 입력해주세요." + '\033[0m')
        continue

      user_num = user_choice_to_num(user_input)
      com_num = r.randint(1, 3)

      result = game(com_num, user_num)

      print()
      print("[$] 가위!", end="\r")
      time.sleep(1)
      print("[$] 바위!!", end="\r")
      time.sleep(1)
      print("[$] 보!!!!!", end="\r")
      time.sleep(1)
      print("        " * 10)

      if result == "무승부":
        print('\033[38;2;255;150;0m' + f"엘리 [{com_choice(com_num)}] : [{com_choice(user_num)}] {user_name}" + '\033[0m' + " 서로 '무승부' 입니다!")
      elif result == "승리":
        print('\033[38;2;255;150;0m' + f"엘리 [{com_choice(com_num)}] : [{com_choice(user_num)}] {user_name}" + '\033[0m' + "님이 " + '\033[38;2;20;170;0m' + "'승리'" + '\033[0m' + "하였습니다!")
        user_score += 1
      else:
        print("" + '\033[38;2;255;150;0m' + f"엘리 [{com_choice(com_num)}] : [{com_choice(user_num)}] {user_name}" + '\033[0m' + "님은 " + '\033[38;2;220;30;0m' + "'패배'" + '\033[0m' + "하였습니다!")
        com_score += 1

      print(f"\n[현재 스코어] - ◆ " + '\033[38;2;255;150;0m' + f" 엘리 {com_score} : {user_score} {user_name}" + '\033[0m' + " ◆")

    if user_score == 2:
      print(f"■ {user_name}님이 삼세판 게임에서 " + '\033[38;2;20;170;0m' + "[최종 승리]" + '\033[0m' + "하였습니다! ■")
      user_coin += bet_coin
    else:
      print(f"■ {user_name}님이 삼세판 게임에서 " + '\033[38;2;220;30;0m' + "[최종 패배]" + '\033[0m' + "하였습니다! ■")
      user_coin -= bet_coin

    if user_coin == 0:
      user_life -= 1
      if user_life >= 1:
        time.sleep(2)
        print("엘리 : 에고.. 말도 없이 게임만 했네...")
        time.sleep(2)
        print("엘리 : 뭐야? 올인이었어? 하하하")
        if user_name == "호구":
          time.sleep(2)
          print("엘리 : 닉값하는군...하하")
        else:
          time.sleep(2)
          print("엘리 : 어떡하니?")
        time.sleep(2)
        print("엘리 : 코인 더 가져오면 또 놀아줄께~")
      else:
        time.sleep(2)
        print("엘리 : 너랑 게임하면 시간 가는줄도 모르겠네, 흐흐")
        time.sleep(2)
        print("엘리 : 뭐야?? 또 올인이었어??")
        if user_name == "호구":
          time.sleep(2)
          print("엘리 : 닉네임이 이제 안쓰럽게 느껴지네...")
        else:
          time.sleep(2)
          print("엘리 : 다음부턴 닉네임 '호구'라고 적는게 어때?")

      time.sleep(2)
      if user_life >= 1:
        print('\033[38;2;220;30;0m' + "코인을 모두 소진하였습니다. 게임을 종료합니다." + '\033[0m')
        print('\033[38;2;255;150;0m' + "Tip. 다시 로그인 해보세요~." + '\033[0m')
        break
      else:
        print('\033[38;2;220;30;0m' + "코인을 모두 소진하였습니다. 게임을 종료합니다." + '\033[0m')
        print('\033[38;2;255;150;0m' + "Tip. 다른 계정을 생성하여 로그인이 가능합니다." + '\033[0m')
        break

  saveUser(userInfo, user_coin, user_life)
  print(f"{user_name}님이 게임에서 퇴장합니다.")
  print('\033[38;2;255;150;0m' + random_ment + '\033[0m')
  exit()

print("엘리와 함께 하는 가위, 바위, 보 게임에 오신 것을 환영합니다~!!!")
main()
