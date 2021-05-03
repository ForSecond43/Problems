import PySimpleGUI as sg
import gspread
import hashlib

###############################################################################################
#                        Database (google sheets)
###############################################################################################

def database(dados):  #function that will add the values to database
    gc = gspread.service_account(filename="Credenciais.json") #will read the json data from the credentials downloaded from the google console
    sh = gc.open_by_key('1Wrsej1yftA9Prh0Mm7sztV2xwK_15Qqjaxjay1Wrbws') #open the desired sheet
    worksheet = sh.sheet1 #select the sheet1
    idssheet = worksheet.col_values(1) #see how many accounts are already registered
    dados['id'] = len(idssheet)+1 #adds one more to the total number of accounts created to have the correct id
    password_hash = hashlib.md5( dados['password'].encode() ).hexdigest() #we will transform the password from text to hash with encryption
    data = [dados['id'], dados['email'], password_hash] #joins all the necessary data in a list
    worksheet.append_row(data) #add the elements of the "data" list to the next line in the sheets

def comparar(email,pwd): #this function will check if the login data has been entered correctly.
    gc = gspread.service_account(filename="Credenciais.json") #will read the json data from the credentials downloaded from the google console
    sh = gc.open_by_key('1Wrsej1yftA9Prh0Mm7sztV2xwK_15Qqjaxjay1Wrbws') #open the desired sheet
    worksheet = sh.sheet1 #select the sheet1
    emailsheet = worksheet.col_values(2) #select all the emails -> column 2

    for index , emails in enumerate(emailsheet):#through a for we will go through the list obtained from the sheets with all emails to be able to compare with the one that was introduced.
        if email == emails: #if the email matches what was entered
            Line = index + 1 #save the id 
            print(Line)
            account_test = True #set the test variable to true to ensure that the email has been entered well
            break #get out of the loop
        else:
            account_test = False #set the test variable to false if the email does not match any of those that have already been registered
            continue

    if account_test == False: #if variable remains false it means that the email does not match
        account_test = True #reset the "account_test"
        return False       #return false to exit the function

    values = worksheet.row_values(Line) #if the email matches we have to import the elements of the line obtained in the "for"
    print(values)
    password_hash_login = hashlib.md5( pwd.encode() ).hexdigest() #we have to encrypt the password entered by the user
    if password_hash_login == values[2]: #compare the two hashes to see if it matches
        return True #return true if all data match
    else:
        return False #return false if not match

def check_mail_exist(email): #this function check if the email is already registered
    gc = gspread.service_account(filename="Credenciais.json") #will read the json data from the credentials downloaded from the google console
    sh = gc.open_by_key('1Wrsej1yftA9Prh0Mm7sztV2xwK_15Qqjaxjay1Wrbws') #open the desired sheet
    worksheet = sh.sheet1 #select the sheet1
    emailsheet = worksheet.col_values(2) #select all the emails -> column 2

    if email in emailsheet: #we only check if the email entered in the "signup" is in the imported list of the emails already registered.
        return True #return true if the email exist
    else:
        return False #return false if the email not exist


############################################################################################################
#                               PYSIMPLEGUI - Windows, inputs
############################################################################################################

def janela_login_signup(): #this function will create the login window
    sg.theme(theme)
    
    layout = [ #here we introduce all the fields we need from "labels" to "inputs" and "buttons"
        [sg.Text('Login', justification= 'center', font='Courier 20', size = (45,1) )],
        [sg.Text('')],
        [sg.Text('Username', size=(8,1)), sg.Input(size=(30,1), key='email_login', do_not_clear= False )],
        [sg.Text('Password',size=(8,1)), sg.Input(size=(30,1), key='pwd_login', password_char='*',do_not_clear= False )],
        [sg.Text('Se não tiver conta, carregue em "Registrar"'), sg.Button('Registrar',size=(8,1) ,border_width=0)],
        [sg.Text('')],
        [sg.Text(' '*25), sg.Button('Login',size=(9,1) , border_width=0, font = 'Courier', button_color= ('white','green'))]
    ]

    return sg.Window('Login', layout=layout, size=(400,250), finalize=True) #returns the window settings

def janela_registro(): #this function will create the signup window
    sg.theme('Reddit')

    layout = [ #here we introduce all the fields we need from "labels" to "inputs" and "buttons"
        [sg.Text('Registo', justification= 'center',size=(45,1),font='Courier 20')],
        [sg.Text('')],
        [sg.Text('Username',size=(8,1)), sg.Input(size=(30,1), key='email_signup', do_not_clear= False)],
        [sg.Text('Password', size=(8,1)), sg.Input(size=(30,1), key='pwd_signup', password_char='*', do_not_clear= False)],
        [sg.Text('')],
        [sg.Text(' '*16),sg.Button('Voltar', size=(10,1), border_width=0) ,sg.Text(' '*2), sg.Button('Sign Up', size=(10,1), border_width=0)]
    ]

    return sg.Window('Sign Up', layout = layout, finalize=True , size=(400,250)) #returns the window settings


janela_login, janela_signup = janela_login_signup(), None #we start the login window

while True: #we use an infinite loop
    window, eventos, valores = sg.read_all_windows() #here we read all the windows, as well as all the events and values entered
    
    if window == janela_login and eventos == sg.WIN_CLOSED: #tests whether the window has been closed
        break
    
    if window == janela_signup and eventos == sg.WIN_CLOSED: #tests whether the window has been closed
        break

    if window == janela_login and eventos == 'Registrar': #if you are in the login window and click on the "register" button
        janela_signup = janela_registro() #show the signup window
        janela_login.hide() #hide the login window

    if window == janela_signup and eventos == 'Voltar': #if you are in the signup window and click on the "voltar" button
        janela_signup.hide() #hide the signup window
        janela_login.un_hide() #un hide the login window

    if window == janela_signup and eventos == 'Sign Up': #if you are in the signup window and click on the "Sign Up" button
        mail_check = check_mail_exist(valores['email_signup']) #let's evoke the function of checking if the email already exists
        if valores['email_signup'] == '' or valores['pwd_signup'] == '' or mail_check: #if the email or password field is empty or the email_check is "true"
            sg.popup('Tem de inserir um email ou password válida ou o email inserido já existe!') #Error message
        
        else: #otherwise
            sg.popup('Conta criada com sucesso') #popup with the message "criado com sucesso"
            janela_signup.hide() #back to the login window
            janela_login.un_hide()

            dict_account = {     #create a dictionary with the data entered
                'email' : valores['email_signup'],
                'password' : valores['pwd_signup']
                }
            database(dict_account) #evokes the function to add the arguments to the database

    if window == janela_login and eventos == 'Login': #if you are in the login window and click on the "login" button
        state = comparar(valores['email_login'], valores['pwd_login']) #evokes the function to check the arguments are correct
        if state: #if state is "true" it means everything is correct
            janela_login.hide() #hide the login window
            janela_atividade = to_do(valores['email_login']) #go to next window
        else: 
            sg.popup('Email ou Password incorreto! Tente novamente :P') # popup de wrong

window.close()  #close the window