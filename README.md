# 데이터통신 프로그래밍 과제: CSMA/CD 구현


프로그램 언어 python
프로그램 제작환경 windows 10
실행방법
실행코드의 압축을 원하는 곳에서 해제하고 python 실행툴로 실행시킨다.


(시뮬레이션 환경 및 구성요소) 다음과 같은 실험환경을 구성한다. 4개의 노드와 Link
(Common Carrier, BUS)는 Thread로 동작하며, 각각의 객체는 다음의 기능을 수행한다.  

 (1) 4개 노드: 각각의 노드는 임의의 시간에 임의의 상대 노드에게 5msec data를 전송한
다. 예를들어 노드1이 노드2에게 Sytem Clock 12msec인 시점에 전송권한을 획득했다
면 그 즉시 5msec data를 전송하며 System Clock 은 17msec으로 업데이트 된다. 만약
노드1이 전송권한을 획득하지 못했다면 Exponential Back-off 알고리즘을 수행하여 얻
은 Random Time 이후에 재전송 요청을 한다. 한편, 노드2는 전송받는 시간만큼은 전
송권한을 갖지 못하며, 전송요청은 전송받은 후 재시도 한다.   

(2) Link: 전역변수 혹은 임의의 객체인 System Clock을 유지,관리,업데이트 하고, 4개 노
드의 전송요청을 관리한다.. 프로그램이 수행되면 System Clock을 수행시키고 임의의
시점에서 노드들의 전송요청을 관리하여 전송요청 승인 또는 거부한다. 즉, Link가 Idle
인 시점에서 임의의 노드가 전송요청을 하는 경우, 전송을 승인하여 전송을 승인하며
System Clock을 업데이트 한다.  

2. (시뮬레이션 시나리오) 다음과 같은 실험 시나리오를 수행하여 각각의 구성요소 별 Log를
기록한다. 즉, 4개 노드와 Link는 각각 모든 이벤트를 Node1.txt, Node2.txt, Node3.txt,
Node4.txt, Link.txt에 기록한다.  

(1) 시나리오: 프로그램 시작후, 모든 Thread가 동작하며 System Clock 0sec에서 시작된다. 전송데이터 크기는 5msec 이며, 임의의 노드에서 다른노드로 임의의 시점에 전송요청
된다. 모든 구성요소들은 CSMA/CD 프로토콜을 따르며, Carrier Sensing의 기능은 각각
의 노드가 Link가에 전송요청 승인/거부로 구현한다. 데이터 전송외의 다른 delay는 없다


Error or Additional Message Handling 에 대한 사항 설명
없음

Additional Comments: 추가로 과제제출관련 언급할내용 작성 

1. 쓰레드의 첫 실행과 작업 1개의 종료시 랜덤으로 시작하기 위해 backofftimer 함수의 결과를 각 노드의 초기값으로 넣는다.

- 쓰레드의 첫 시작과 작업 1개 종료시 backofftime의 파라미터: 4 (고정)
- 링크가 사용중이어서 backofftime을 실행시킬 경우의 파라미터: 재전송 횟수

2. sender와 receiver가 전송도중 전송요청하지 않도록 backofftime을 감소시키지 않는다.

