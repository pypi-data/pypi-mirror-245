try: 
    from tc_data import tc_message
except:
    pass
from common.util import LoadThread
from threading import Event
from time import sleep

sync_INVITE_14 = Event()
sync_ACK_17 = Event()
sync_INVITE_18 = Event()
sync_ACK_21 = Event()
sync_REFER_22 = Event()
sync_INVITE_27 = Event()
sync_ACK_29 = Event()
sync_NOTIFY_37 = Event()
sync_REFER_40 = Event()
sync_NOTIFY_43 = Event()
sync_SUBSCRIBE_55 = Event()
sync_NOTIFY_63 = Event()
sync_SUBSCRIBE_67 = Event()
sync_BYE_68 = Event()
sync_NOTIFY_73 = Event()
sync_NOTIFY_84 = Event()
sync_SUBSCRIBE_89 = Event()
sync_BYE_90 = Event()

def sip_flow(): # main sip function name must be sip_flow
    SUB_A_thread = LoadThread(target=SUB_A_flow, daemon=True)
    SUB_B_thread = LoadThread(target=SUB_B_flow, daemon=True)
    SUB_A_thread.start()
    SUB_B_thread.start()
    SUB_A_thread.join()
    SUB_B_thread.join()

def SUB_A_flow():
    sync_INVITE_14.wait(60)
    sync_ACK_17.wait(60)
    sync_INVITE_18.wait(60)
    sync_ACK_21.wait(60)
    sync_REFER_22.wait(60)

    m_INVITE__27 = SUB_A.send_new(message_string=tc_message["INVITE #27"])
    sync_INVITE_27.set()
    SUB_A.wait_for_message("200 OK")
    SUB_A.send(tc_message["ACK #29"])
    sync_ACK_29.set()

    m_NOTIFY__37 = SUB_A.send_new(message_string=tc_message["NOTIFY #37"])
    sync_NOTIFY_37.set()
    SUB_A.wait_for_message("200 OK")
    sync_REFER_40.wait(60)
    SUB_A.send(tc_message["NOTIFY #43"])
    sync_NOTIFY_43.set()
    SUB_A.wait_for_message("200 OK")
    sync_SUBSCRIBE_55.wait(60)
    SUB_A.send(tc_message["NOTIFY #63"])
    sync_NOTIFY_63.set()
    SUB_A.wait_for_message("200 OK")
    sync_SUBSCRIBE_67.wait(60)
    sync_BYE_68.wait(60)
    SUB_A.send(tc_message["NOTIFY #73"])
    sync_NOTIFY_73.set()
    SUB_A.wait_for_message("200 OK")
    SUB_A.send(tc_message["NOTIFY #84"])
    sync_NOTIFY_84.set()
    SUB_A.wait_for_message("200 OK")
    sync_SUBSCRIBE_89.wait(60)
    sync_BYE_90.wait(60)


def SUB_B_flow():

    m_INVITE__14 = SUB_B.wait_for_message("INVITE")
    sync_INVITE_14.set()
    SUB_B.send(tc_message["100 Trying #15"])
    SUB_B.send(tc_message["302 Moved Temporarily #16"])

    m_ACK__17 = SUB_B.wait_for_message("ACK")
    sync_ACK_17.set()

    m_INVITE__18 = SUB_B.wait_for_message("INVITE")
    sync_INVITE_18.set()
    SUB_B.send(tc_message["100 Trying #19"])
    SUB_B.send(tc_message["200 OK #20"])

    m_ACK__21 = SUB_B.wait_for_message("ACK")
    sync_ACK_21.set()

    m_REFER__22 = SUB_B.wait_for_message("REFER")
    sync_REFER_22.set()
    SUB_B.send(tc_message["100 Trying #23"])
    SUB_B.send(tc_message["202 Accepted #25"])
    sync_INVITE_27.wait(60)
    sync_ACK_29.wait(60)
    sync_NOTIFY_37.wait(60)

    m_REFER__40 = SUB_B.wait_for_message("REFER")
    sync_REFER_40.set()
    SUB_B.send(tc_message["100 Trying #41"])
    sync_NOTIFY_43.wait(60)
    SUB_B.send(tc_message["202 Accepted #46"])

    m_SUBSCRIBE__55 = SUB_B.wait_for_message("SUBSCRIBE")
    sync_SUBSCRIBE_55.set()
    SUB_B.send(tc_message["200 OK #58"])
    sync_NOTIFY_63.wait(60)

    m_SUBSCRIBE__67 = SUB_B.wait_for_message("SUBSCRIBE")
    sync_SUBSCRIBE_67.set()

    m_BYE__68 = SUB_B.wait_for_message("BYE", dialog=m_INVITE__14.get_dialog())
    sync_BYE_68.set()
    SUB_B.reply_to(m_SUBSCRIBE__67, tc_message["200 OK #69"])
    SUB_B.reply_to(m_BYE__68, tc_message["200 OK #70"])
    sync_NOTIFY_73.wait(60)
    sync_NOTIFY_84.wait(60)

    m_SUBSCRIBE__89 = SUB_B.wait_for_message("SUBSCRIBE", dialog=m_SUBSCRIBE__55.get_dialog())
    sync_SUBSCRIBE_89.set()

    m_BYE__90 = SUB_B.wait_for_message("BYE")
    sync_BYE_90.set()
    SUB_B.reply_to(m_SUBSCRIBE__89, tc_message["200 OK #91"])
    SUB_B.reply_to(m_BYE__90, tc_message["200 OK #92"])


def csta_flow(): # main csta function name must be csta_flow
    csta_app_thread = LoadThread(target=CSTA_app_flow, daemon=True)
    csta_app_thread.start()
    SUB_A_csta_thread = LoadThread(target=SUB_A_csta_flow, daemon=True)
    SUB_B_csta_thread = LoadThread(target=SUB_B_csta_flow, daemon=True)
    SUB_A_csta_thread.start()
    SUB_B_csta_thread.start()
    SUB_A_csta_thread.join()
    SUB_B_csta_thread.join()
    csta_app_thread.join()

def CSTA_app_flow():
    pass

def SUB_A_csta_flow():
    pass

def SUB_B_csta_flow():
    pass
