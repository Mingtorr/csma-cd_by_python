import threading
import threading as tread
import random

lock_Link = threading.Lock()


class Node:
    def __init__(self, id):
        self.id = id
        self.backoffTime = BackoffTimer(4)
        self.exec_time = 0  # 실행시간 관리
        self.retrans_num = 0  # 재전송 횟수
        self.log = []

    def set_BackoffTimer(self, time):
        self.backoffTime = time


class Link:
    def __init__(self, n1, n2, n3, n4):
        self.systemClock = 0
        self.nodes = []
        self.nodes.append(n1)
        self.nodes.append(n2)
        self.nodes.append(n3)
        self.nodes.append(n4)
        self.sender = -1
        self.receiver = -1
        self.log = []

    def Increase_systemClock(self):
        self.systemClock += 1

    def Decrease_backofftime(self):  # sender와 receiver 제외하고 backofftime 감소
        for node in self.nodes:
            if node.id != self.sender and node.id != self.receiver:
                node.backoffTime -= 1

    def CheckBackofftime(self):
        for node in self.nodes:
            if node.backoffTime <= 0:
                if node.id != self.sender and node.id != self.receiver:
                    return node.id
        return -1


def timer(time):  # 과제 출력 양식으로 시간을 바꾸는 함수
    min, reaminder = divmod(time, 60*1000)
    sec, msec = divmod(reaminder, 1000)
    rtn = ('{:02}:{:02}:{:03}'.format(min, sec, msec))
    return rtn


def BackoffTimer(transNum):  # backofftimer를 만드는 함수
    temp = min(transNum, 10)
    rand_num = (int)(random.random() * (pow(2, temp) - 1))
    return rand_num


def csma_cd(node, link):

    while link.systemClock < 60000:
        # critical section 시간 증가 및 감수
        lock_Link.acquire()

        # 6만 이상의 값 끝내기
        if link.systemClock >= 60000:
            if link.sender != -1:
                while True:
                    if link.nodes[link.sender].exec_time >= 5:
                        # 6만 이후 종료된 노드 전송종료 출력
                        link.log.append(str(timer(link.systemClock)) + ' Node' + str(link.sender+1) + ' Data Send Finished To Node' + str(link.receiver+1))
                        link.nodes[link.sender].log.append(str(timer(link.systemClock)) + ' Data Send Finished To Node'+str(link.receiver+1))
                        link.nodes[link.receiver].log.append(str(timer(link.systemClock)) + ' Data Receive Finished from Node'+str(link.sender+1))
                        link.sender = -1
                        break
                    else:
                        link.nodes[link.sender].exec_time += 1
                        link.Increase_systemClock()
        else:
            link.Decrease_backofftime()
            link.Increase_systemClock()
        lock_Link.release()

        # reminder section
        if link.systemClock >= 60001:
            continue
        if link.sender != -1:  # 실행중인 노드가 있으면
            link.nodes[link.sender].exec_time += 1
            if link.nodes[link.sender].exec_time == 5:  # 실행시간이 5에 도달시
                # 전송 종료 출력
                link.log.append(str(timer(link.systemClock)) + ' Node' + str(link.sender+1) + ' Data Send Finished To Node' + str(link.receiver+1))
                link.nodes[link.sender].log.append(str(timer(link.systemClock)) + ' Data Send Finished To Node'+str(link.receiver+1))
                link.nodes[link.receiver].log.append(str(timer(link.systemClock)) + ' Data Receive Finished from Node'+str(link.sender+1))

                # 전송데이터 초기화
                link.nodes[link.sender].exec_time = 0
                link.nodes[link.sender].set_BackoffTimer(BackoffTimer(4))
                link.sender = -1
                link.receiver = -1

        tmp = link.CheckBackofftime()  # 백오프타임이 0인 노드 체크
        if tmp != -1:
            # 랜덤으로 하나 뽑기
            rand_num = [0, 1, 2, 3]
            rand_num.remove(tmp)
            dest = random.choice(rand_num)
            # 전송 요청 출력
            link.log.append(str(timer(link.systemClock)) + ' Node' + str(tmp+1) + ' Data Send Request To Node' + str(dest+1))
            link.nodes[tmp].log.append(str(timer(link.systemClock)) + ' Data Send Request To Node'+str(dest+1))

            if link.sender != -1:  # 전송중인 노드가 있을경우
                link.nodes[tmp].retrans_num += 1
                link.nodes[tmp].set_BackoffTimer(BackoffTimer(link.nodes[tmp].retrans_num))
                # 전송 거절 출력
                link.log.append(str(timer(link.systemClock)) + ' Reject: Node' + str(tmp+1)+' Data Send Request To Node'+str(dest+1))
                link.nodes[tmp].log.append(str(timer(link.systemClock)) + ' Data Send Request Reject from Link')
                link.nodes[tmp].log.append(str(timer(link.systemClock)) + ' Exponential Back-off Time: '+str(link.nodes[tmp].backoffTime) + ' msec')

            else:
                link.sender = tmp
                link.receiver = dest
                link.nodes[tmp].retrans_num = 0
                # 전송 승인 출력
                link.log.append(str(timer(link.systemClock)) + ' Accept: Node' + str(tmp+1)+' Data Send Request To Node'+str(dest+1))
                link.nodes[tmp].log.append(str(timer(link.systemClock)) + ' Data Send Request Accept from Link')
                link.nodes[dest].log.append(str(timer(link.systemClock)) + ' Data Receive Start from Node'+str(tmp+1))
    # 종료이후


if __name__ == '__main__':
    nodes = []
    nodes.append(Node(0))
    nodes.append(Node(1))
    nodes.append(Node(2))
    nodes.append(Node(3))

    link = Link(nodes[0], nodes[1], nodes[2], nodes[3])
    threads = []
    threads.append(tread.Thread(target=csma_cd, args=(nodes[0], link)))
    threads.append(tread.Thread(target=csma_cd, args=(nodes[1], link)))
    threads.append(tread.Thread(target=csma_cd, args=(nodes[2], link)))
    threads.append(tread.Thread(target=csma_cd, args=(nodes[3], link)))

    for i in nodes:
        i.log.append(str(timer(link.systemClock)) + ' Node' + str(i.id+1) + ' Start //00 min 00 sec 000msec')
    link.log.append(str(timer(link.systemClock)) + ' Link Start //00 min 00 sec 000msec')
    link.log.append(str(timer(link.systemClock)) + ' System Clock Start //00 min 00 sec 000msec')

    # 쓰레드 시작
    for i in threads:
        i.start()

    for i in threads:
        i.join()

    for i in nodes:
        i.log.append(str(timer(link.systemClock)) + ' Node'+str(i.id+1)+' Finished')
    link.log.append(str(timer(link.systemClock)) + ' System Clock Finished')
    link.log.append(str(timer(link.systemClock)) + ' Link Finished')

    # 노드 파일에 쓰기
    for i in nodes:
        dst = 'Node' + str(i.id+1)+'.txt'
        f = open(dst, 'w+')
        for j in i.log:
            data = j+'\n'
            f.write(data)
        f.close()

    # 링크 파일에 쓰기
    f = open("link.txt", 'w+')
    for i in link.log:
        data = i+"\n"
        f.write(data)
    f.close()
    print('작업완료')
