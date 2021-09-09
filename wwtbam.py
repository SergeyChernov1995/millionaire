# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------------
# Who Wants To Be A Millionaire?
# Copyright © 2021 Sergey Chernov aka Gamer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import time
from PIL import Image, ImageTk, ImageDraw, ImageFont
from random import randint
from random import choice
from random import randrange
from enum import Enum
import codecs
root = tk.Tk()
root.geometry("800x600")
root.title("КХСМ")
_5050_usedonthisq = False
_5050_del = []
lifelines = [True, True, True]
lifeline_buttons = []
root.resizable(width=False, height=False)
#root["bg"] = "#7f7f7f"
dough_file = codecs.open('moneytree.txt', 'r', "utf_8_sig")
log = codecs.open('log.txt', 'a', "utf_8_sig")
money = []
for line in dough_file:
    f = int(line.rstrip("\n"))
    money.append(f)
money.append(0)
dough_file.close()
money = money[::-1]
#print(money)
q = money[1:len(money)-1:1]
milestone = []
risky_milestone = ttk.Combobox(root, values=q, width=10)
risky_milestone.state = 'readonly'
risky_milestone.current(9)
current_q_number = 0
preguntas_ultimately = []
ordnung_vor_frage = 0
preguntas = {}
vyberite = tk.Label(root, text="Выберите несгораемую сумму")
pole_q = ttk.LabelFrame(root, height=340, width=500)
pole_voprosa = None
polya_variantov = []
accepted = None
dd_accepted = []
class st(Enum):
    before_answer = 1
    answered = 2
    walked = 3
    dd = 4
    check_after_walkaway = 5
    dd_secondattempt = 6
    dd_1wrong = 7

stage = st.before_answer


def start_risk():
    global milestone
    milestone.append(risky_milestone.current()+1)
    log.write("Выбранная несгораемая сумма: "+str(money[milestone[0]])+'\n')
    setup_lifelines(len(lifelines))
    start()


def doSomething():
    if tk.messagebox.askyesno("Exit", "Do you want to quit the application?"):
        log.close()
        root.destroy()


def reveal(a):
    global preguntas_ultimately, ordnung_vor_frage, current_q_number, milestone, stage
    root.after_cancel(root.check_answer)
    choose_game_label.place_forget()
    polya_variantov[preguntas_ultimately[ordnung_vor_frage]["C"]-1]["bg"]="#00ff3f"
    log.write("Правильный ответ: "+letter(preguntas_ultimately[ordnung_vor_frage]["C"]-1)+'\n')
    if (a==preguntas_ultimately[ordnung_vor_frage]["C"]):
        if (stage == st.answered):
            tk.messagebox.showinfo("Верно!", "Вы дали правильный ответ!")
            pole_q.place_forget()
            show_tree(current_q_number)
        elif (stage==st.check_after_walkaway):
            tk.messagebox.showinfo("Верно!", "Вы напрасно остановились!")
            log.write("Выигрыш: "+str(money[current_q_number-1])+'\n')
    else:
        if (stage == st.answered):
            i = current_q_number
            while True:
                i -= 1
                if (i == 0) or (i in milestone):
                    break
            tk.messagebox.showerror("Неверно!", "Вы ошиблись, и ваш выигрыш - "+str(money[i]))
            log.write("Выигрыш: " + str(money[i]) + '\n')
        elif (stage==st.check_after_walkaway):
            tk.messagebox.showinfo("Браво!", "Вы вовремя остановились!")
            log.write("Выигрыш: " + str(money[current_q_number - 1])+'\n')


def dd_1w(a):
    global stage, accepted, preguntas_ultimately, ordnung_vor_frage
    root.after_cancel(root.wr)
    polya_variantov[a]["bg"] = "#7f7f7f"
    stage = st.dd_secondattempt


def letter(e):
    if (e==0):
        return ("A")
    elif(e==1):
        return("B")
    elif(e==2):
        return("C")
    else:
        return("D")



def answer(a):
    global stage, accepted, preguntas_ultimately, ordnung_vor_frage, dd_accepted
    if (stage == st.before_answer):
        #print(a+1)
        stage = st.answered
        polya_variantov[a]["bg"]="#ff7f00"
        accepted = a+1
        for b in range(len(lifeline_buttons)):
            lifeline_buttons[b]["state"] = "disabled"
        walkaway["state"] = "disabled"
        log.write('Ответ игрока: '+letter(a)+'\n')
        root.check_answer = root.after(2500, lambda i=accepted: reveal(i))
    elif (stage == st.walked):
        polya_variantov[a]["bg"]="#ff7f00"
        accepted = a+1
        root.check_answer = root.after(2500, lambda i=accepted: reveal(i))
        log.write('Предполагаемый ответ: ' + letter(a) + '\n')
        stage = st.check_after_walkaway
    elif (stage == st.dd):
        polya_variantov[a]["bg"] = "#ff7f00"
        accepted = a + 1
        dd_accepted.append(a)
        log.write('Первый ответ: ' + letter(a) + '\n')
        if (accepted == preguntas_ultimately[ordnung_vor_frage]["C"]):
            stage=st.answered
            root.check_answer = root.after(2500, lambda i=accepted: reveal(i))
        else:
            stage=st.dd_1wrong
            root.wr = root.after(2500, lambda i=accepted: dd_1w(i-1))
    elif (stage==st.dd_secondattempt):
        if (a not in dd_accepted):
            log.write('Второй ответ: ' + letter(a) + '\n')
            polya_variantov[a]["bg"]="#ff7f00"
            accepted = a+1
            stage = st.answered
            root.check_answer = root.after(2500, lambda i=accepted: reveal(i))
    pass #dopisat'

def lifeline_used(a):
    global _5050_usedonthisq, ordnung_vor_frage, preguntas_ultimately, current_q_number, iq, _5050_del, stage
    if (a==0):
        _5050_usedonthisq = True
        _5050_del = []
        _5050_rem = []
        log.write("Игрок берёт подсказку 50 на 50. Остаются варианты ")
        for t in range(2):
            while True:
                k = randint(0, 3)
                if (k not in _5050_del) and (k+1!=preguntas_ultimately[ordnung_vor_frage]["C"]):
                    _5050_del.append(k)
                    break
        for t in range(4):
            if (t in _5050_del):
                polya_variantov[t]["text"] = ""
                polya_variantov[t]["state"] = "disabled"
            else:
                _5050_rem.append(t)
                log.write(letter(t))
                if (len(_5050_rem)==1):
                    log.write(" и ")
                else:
                    log.write("."+"\n")

        lifeline_buttons[0]["state"] = "disabled"
        lifelines[0]=False
    elif (a==1):
        log.write("Игрок берёт подсказку Звонок другу: друг ")
        iq = []
        iq.append(oddz_paf[current_q_number]["K"])
        iq.append(oddz_paf[current_q_number]["GC"])
        iq.append(oddz_paf[current_q_number]["GR"])
        iq.append(oddz_paf[current_q_number]["N"])
        iq.append(oddz_paf[current_q_number]["N1"])
        iq.append(oddz_paf[current_q_number]["N2"])
        if (_5050_usedonthisq is True):
            m = randint(1, sum(iq[:4]))
        else:
            m = randint(1, sum(iq))
        if (m<=iq[0]):
            tkinter.messagebox.showinfo("Друг", "Правильный ответ - "+preguntas_ultimately[ordnung_vor_frage]["A"][preguntas_ultimately[ordnung_vor_frage]["C"]-1]+'.'+'\n'+'Я это точно знаю!')
            log.write("не сомневается в правильности варианта "+letter(preguntas_ultimately[ordnung_vor_frage]["C"]-1)+'.\n')
        elif(m<=sum(iq[:2])):
            tkinter.messagebox.showinfo("Друг", "Я думаю, что правильный ответ - " + preguntas_ultimately[ordnung_vor_frage]["A"][
                preguntas_ultimately[ordnung_vor_frage]["C"]-1] + '.')
            log.write("думает, что правильный ответ - "+letter(preguntas_ultimately[ordnung_vor_frage]["C"]-1)+'.\n')
        elif(m<=sum(iq[:3])):
            while True:
                fm=randint(0,3)
                if (polya_variantov[fm]["state"]!="disabled"):
                    break
            tkinter.messagebox.showinfo("Друг", "Я думаю, что правильный ответ - " +preguntas_ultimately[ordnung_vor_frage]["A"][fm] + '.')
            log.write(
                "думает, что правильный ответ - " + letter(fm) + '.\n')
        elif(m<=sum(iq[:4])):
            tkinter.messagebox.showinfo("Друг", "Извини, ничем не могу помочь.")
            log.write("не знает ответа.\n")
        elif(m<=sum(iq[:5])):
            while True:
                fm=randint(0,3)
                if(fm+1!=preguntas_ultimately[ordnung_vor_frage]["C"]):
                    break
            tkinter.messagebox.showinfo("Друг", "Я не знаю ответа, но это точно не "+preguntas_ultimately[ordnung_vor_frage]["A"][fm] + '.')
            log.write("исключает вариант "+ letter(fm) + '.\n')
        else:
            schachlo = []
            for t in range(2):
                while True:
                    fm=randint(0,3)
                    if (fm not in schachlo) and (fm+1!=preguntas_ultimately[ordnung_vor_frage]["C"]):
                        schachlo.append(fm)
                        break
            tkinter.messagebox.showinfo("Друг", "Точно не знаю, но это не "+preguntas_ultimately[ordnung_vor_frage]["A"][schachlo[0]]+" и не "+preguntas_ultimately[ordnung_vor_frage]["A"][schachlo[1]])
            log.write("исключает варианты " + letter(schachlo[0]) + ' и '+ letter(schachlo[1])+ '.\n')
        lifeline_buttons[1]["state"] = "disabled"
        lifelines[1]=False
    elif(a==2):
        log.write("Игрок берёт подсказку Помощь зала. \n")
        zna = aud_odds[current_q_number-1]
        otvet = [0, 0, 0, 0]
        for counter in range(100):
            if (counter<zna):
                otvet[preguntas_ultimately[ordnung_vor_frage]["C"] - 1]+=1
            else:
                while True:
                    am = randint(0, 3)
                    if (am not in _5050_del):
                        break
                otvet[am]+=1
        tkinter.messagebox.showinfo("Результаты голосования", "A: "+str(otvet[0])+"%, B:"+str(otvet[1])+"%, C:"+str(otvet[2])+"%, D:"+str(otvet[3])+"%.")
        log.write("Результаты голосования: "+"A: "+str(otvet[0])+"%, B:"+str(otvet[1])+"%, C:"+str(otvet[2])+"%, D:"+str(otvet[3])+"%.\n")
        lifeline_buttons[2]["state"] = "disabled"
        lifelines[2]=False
    else:
        walkaway["state"] = "disabled"
        log.write("Игрок берёт Право на ошибку.\n")
        for k in range(len(lifeline_buttons)):
            lifeline_buttons[k]["state"] = "disabled"
        lifelines[3]=False
        stage = st.dd
        pass #dopisat'

def life_names(a):
    if (a==0):
        return ("50 на 50")
    elif(a==1):
        return ("Звонок другу")
    elif(a==2):
        return ("Помощь зала")
    elif(a==3):
        return ("Право на ошибку")

def you_yellow():
    global current_q_number, stage
    tkinter.messagebox.showinfo("Вы забрали деньги", "Мы вас поздравляем, вы выиграли "+str(money[current_q_number-1])+' руб.!')
    log.write("Игрок забирает деньги.\n")
    for a in range(len(lifeline_buttons)):
        lifeline_buttons[a]["state"] = "disabled"
        lifeline_buttons[a].place_forget()
    walkaway.place_forget()
    stage = st.walked
    choose_game_label["text"] = "Какой вариант вы бы выбрали, если бы отвечали?"
    pass #dopisat'

def setup_lifelines(a):
    global  lifeline_buttons
    for u in range(a):
        qaz = tk.Button(pole_q, text = life_names(u), width=11, height=1, command = lambda a1 = u: lifeline_used(a1))
        lifeline_buttons.append(qaz)
        lifeline_buttons[u]["state"] = "normal"
    for z in range(a):
        lifeline_buttons[z].place(x=10+118*z, y=220)
    walkaway.place(x=140, y=270)



def start():
    global milestone, current_q_number, preguntas, preguntas_ultimately, ordnung_vor_frage, pole_q, pole_voprosa, polya_variantov, accepted, _5050_usedonthisq, choose_game_label, lifeline_buttons, stage, _5050_del, dd_accepted
    choose_game_label.place(x=160, y=20)
    mil_ch.place_forget()
    risky_milestone.place_forget()
    vyberite.place_forget()
    #print(milestone)
    preguntas_ultimately = []
    pole_voprosa = None
    accepted = None
    _5050_usedonthisq = False
    _5050_del = []
    stage = st.before_answer
    polya_variantov = []
    dd_accepted = []
    if (current_q_number<15):
        current_q_number+=1
        choose_game_label["text"] = str(current_q_number) + ' вопрос и ' + str(
            money[current_q_number]) + ' руб.'
        log.write(str(current_q_number) + ' вопрос (' + str(
            money[current_q_number])+')\n')
        qbase = codecs.open('vopros'+str(current_q_number)+'.txt', 'r', "utf_8_sig")
        for line in qbase:
            var = {}
            aux = line.rstrip("\n")
            var["Q"] = aux
            var["A"] = []
            for a in range(4):
                H = qbase.readline()
                H = H.rstrip('\n')
                var["A"].append(H)
            H = qbase.readline()
            var["C"] = int(H)
            preguntas_ultimately.append(var)
        qbase.close()
        ordnung_vor_frage = randint(0, len(preguntas_ultimately)-1)
        pole_q.place(x=10, y=10)
        pole_voprosa = tk.Label(pole_q,  width=55, height=5)
        pole_voprosa["text"] = preguntas_ultimately[ordnung_vor_frage]["Q"]
        log.write(preguntas_ultimately[ordnung_vor_frage]["Q"]+'\n')
        pole_voprosa["justify"] = tkinter.CENTER
        pole_voprosa["bg"] = "#00007f"
        pole_voprosa["fg"] = "#ffffff"
        pole_voprosa["wraplength"] = 280
        pole_voprosa.place(relx=0.05, rely=0.05)
        for w in range(4):
            i = tk.Button(pole_q, text = preguntas_ultimately[ordnung_vor_frage]["A"][w], width=19, height=1, command = lambda a1 = w: answer(a1))
            log.write(letter(w)+": "+preguntas_ultimately[ordnung_vor_frage]["A"][w]+'\n')
            polya_variantov.append(i)
            polya_variantov[w]["state"] = "normal"
            polya_variantov[w]["bg"] = "#007fff"
            polya_variantov[w]["fg"] = "#ffffff"
        for z in range(2):
            polya_variantov[z].place(x=40+190*z, y=100)
        for z in range(2, 4, 1):
           polya_variantov[z].place(x=40+190*(z % 2), y=140)
        if (current_q_number==1) or (current_q_number-1 in milestone):
            walkaway["state"] = "disabled"
        else:
            walkaway["state"] = "normal"
        for z in range(len(lifeline_buttons)):
            if (lifelines[z]):
                lifeline_buttons[z]["state"] = "normal"
            else:
                lifeline_buttons[z]["state"] = "disabled"
    else:
        choose_game_label.place_forget()
        tkinter.messagebox.showinfo("Поздравляем!", "Вы прошли игру и выиграли "+str(money[-1])+' руб.!')
        log.write("Выигрыш: "+str(money[-1])+'\n')





def choose_game_mode_button():
    global choose_game_mode, milestone, vyberite, choose_game_label, lifelines
    classic.place_forget()
    risky.place_forget()
    var_ch.place_forget()
    if (choose_game_mode.get()==0):
        log.write("Выбранный вариант игры: классический."+'\n')
        #choose_game_label.place_forget()
        milestone.append(5)
        milestone.append(10)
        setup_lifelines(len(lifelines))
        start()
    else:
        choose_game_label["text"] = "Вы выбрали рисковый вариант"
        log.write("Выбранный вариант игры: рисковый." + '\n')
        lifelines.append(True)
        vyberite.place(x=160, y=120)
        mil_ch.place(x=160, y=270)
        risky_milestone.place(x=160, y=170)


def hidetree():
    global tree
    root.after_cancel(root.new)
    tree.place_forget()
    start()




def show_tree(questions_passed):
    global money, milestone, tree
    #back = Image.open('img/tree_bg.png')
    #backg = ImageTk.PhotoImage(back)
    #tree = ttk.LabelFrame(root, height=400, width=180)
    tree.place(x=420, y=20)
    tree_sums = []
    #milestone = [5, 10]
    for a in range(1, len(money), 1):
        b = tk.Label(tree, text=str(a)+(' ')*(15-len(str(a)))+str(money[a]))       #(19-(len(str(money[a]))))+str(money[a]))
        if (a in milestone) or (a==15):
            b["fg"]= "#7f7f7f"
        else:
            b["fg"] = "#ff7f00"
        tree_sums.append(b)
        tree_sums[a-1].place(relx=0.05, rely=1-a/(len(money)-1))
        #c = tk.Label(tree, text=str(money[a]))
        #c.place(relx=0.55, rely=1-a/(len(money)-1))
    #questions_passed = 13
    for a in range(1, questions_passed+1, 1):
        d = list(tree_sums[a-1]["text"])
        d[len(d)//2] = '-'
        tree_sums[a-1]["text"]=''.join(d)
    if (questions_passed>0):
        tree_sums[questions_passed-1]["fg"] = "#000000"
        tree_sums[questions_passed-1]["bg"] = "#ff7f00"
    root.new=root.after(2500, hidetree)



choose_game_label = tk.Label(root, text="Перед началом игры выберите вариант")
choose_game_label.place(x=160, y=20)
choose_game_mode = tk.IntVar()
choose_game_mode.set(0)
classic = ttk.Radiobutton(text='Классический', variable=choose_game_mode, value=0)
risky = ttk.Radiobutton(text='Рисковый', variable=choose_game_mode, value=1)
var_ch = tk.Button(root, text="Выбрать вариант", command=choose_game_mode_button, width=15, height=1)
var_ch.place(x=160, y=220)
mil_ch = tk.Button(root, text="Начать игру", command=start_risk, width=15, height=1)
#var_ch.place(x=160, y=220)
classic.place(x=160, y=120)
risky.place(x=160, y=170)
walkaway = tk.Button(pole_q, text="Взять деньги", command=you_yellow, width=10, height=1)
tree = ttk.LabelFrame(root, height=400, width=180)
oddz_paf = []
fa = codecs.open('phone.txt', 'r', "utf_8_sig")
for line in fa:
    p = {}
    iq = list(map(int, line.split()))
    p["K"] = iq[0] #знаю точно ответ
    p["GC"] = iq[1] #не знаю точно, но догадка верна
    p["GR"] = iq[2] #не знаю точно, говорю наушад
    p["N"] = iq[3] #не знаю
    p["N1"] = iq[4] #не знаю, но один вариант могу исключить
    p["N2"] = iq[5] #не знаю, но могу исключить два варианта
    oddz_paf.append(p)
fa.close()

aud_odds = []
zal = codecs.open('audience.txt', 'r', "utf_8_sig")
for line in zal:
    aud_odds.append(int(line))
zal.close()











root.protocol('WM_DELETE_WINDOW', doSomething)
root.mainloop()