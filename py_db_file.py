import sqlite3

#SQLiteStudio is used for table pre-creation.
connection = sqlite3.connect("USER.db")
print ("open database success")

chyper_u = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
chyper_s = 'TIMEODANSFRBCGHJKLPQUVWXYZ9876543210'

def decr(e_pw):
    iloc=[]
    decr_pw = ''
    e_pw = e_pw.upper()
    for i in e_pw:
        iloc.append(chyper_s.index(i))
    for i in iloc:
      decr_pw = decr_pw + chyper_u[i]
    return decr_pw.swapcase()

def ecp(pw):
    iloc = []
    ecp_pw = ''
    pw = pw.upper()
    for i in pw:
        iloc.append(chyper_u.index(i))
    for i in iloc:
        ecp_pw = ecp_pw + chyper_s[i]
    return ecp_pw


user_check = input("New user? Y/N: ").strip().upper()

if user_check == 'Y':
    print("Create user")
    user_create = input('Enter your ID: ')
    user_pw = input('Enter your password: ')
    user_pw_ecp = ecp(user_pw)
    user_login = (user_create, user_pw_ecp)

    print("(* Your ID:{}, Password: {}, Encrypt PW: {} *)".format(user_create, user_pw, user_pw_ecp))

    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO UserList (id, pw) values (?, ?)", user_login)
    cursor.execute("COMMIT;")
    cursor.close()
    print("Your ID and Password were done")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM UserList;")
    results = cursor.fetchall()
    cursor.close()

#    for r in results:
#        print(r)

elif user_check == 'N':
    print("Login")
    user_id = input("Enter your id: ")
    user_pw = input("Enter your password: ")
    decr_pw = decr(user_pw)
    connection = sqlite3.connect("USER.db")
    print("* DB Connected *")
    print('*',user_id, user_pw, decr_pw, ecp(decr_pw),'*') # there is a bug for the password case
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM UserList WHERE id = ?", (user_id,))
    data = cursor.fetchall()

    if len(data) == 0:
        print('Wrong ID or Password! (* ID "%s" does not exist *)' % user_id)
    else:
        cursor.execute("SELECT id, pw FROM UserList WHERE id = ? AND pw = ?", (user_id, decr_pw,))
        data = cursor.fetchall()

        if len(data) == 0:
            print('Wrong ID or Password!')
        else:
            print("Welcome! *Logout*")
    cursor.close()

else:
    print("Error enter, bye!")