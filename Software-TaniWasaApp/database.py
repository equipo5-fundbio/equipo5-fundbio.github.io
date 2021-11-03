import sqlite3

def nuevopaciente(dni, nom, apll, mail, pwd, tel, nac, sex, proc, peso, alt, centro, riss, comorb, med):
    conn = sqlite3.connect('TW.db')
    cursor = conn.cursor()
    
    conn.execute("INSERT INTO pacientes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (dni, nom, apll, mail, pwd, tel, nac, sex, proc, peso, alt, centro, riss, comorb, med))
    conn.commit()
    conn.close()

def infopaciente(dni):
    conn = sqlite3.connect('TW.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM pacientes WHERE Dni = ?", (dni,))
    resultado = cursor.fetchone()
    conn.commit()
    conn.close()
    return resultado
    #si no está registrado resultado = None
    
#introducir los nuevos datos
def editpaciente(dni, nom, apll, mail, pwd, tel, nac, sex, proc, peso, alt, centro, riss, comorb, med):
    conn = sqlite3.connect('TW.db')
    cursor = conn.cursor()
    
    cursor.execute("UPDATE pacientes SET Nom = ?, Apll = ?, Mail = ?, Pwd = ?, Tel = ?, Nac = ?, Sex = ?, Proc= ?, Peso = ?, Alt = ?, Centro = ?,Riss = ?, Comorb = ?, Med = ? WHERE Dni = ?", (nom, apll, mail, pwd, tel, nac, sex, proc, peso, alt, centro, riss, comorb, med, dni))
    
    conn.commit()
    conn.close()

def nuevomedico(dni, nom, apll, mail, pwd, tel, pac):
    conn = sqlite3.connect('TW.db')
    cursor = conn.cursor()
    
    conn.execute("INSERT INTO medicos VALUES (?, ?, ?, ?, ?, ?)", (dni, nom, apll, mail, pwd, tel))
    conn.commit()
    conn.close()
    
def infomedico(dni):
    conn = sqlite3.connect('TW.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM medicos WHERE Dni = ?", (dni,))
    resultado = cursor.fetchone()
    conn.commit()
    conn.close()
    return resultado
    
def pacmedico(dnidoc):
    conn = sqlite3.connect('TW.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM pacientes WHERE Med = ?", (dnidoc,))
    resultado = cursor.fetchall()
    conn.commit()
    conn.close()
    return resultado
    
#introducir los nuevos datos
def editmedico(dni, nom, apll, mail, pwd, tel):
    conn = sqlite3.connect('TW.db')
    cursor = conn.cursor()
    
    cursor.execute("UPDATE medicos SET Nom = ?, Apll = ?, Mail = ?, Pwd = ?, Tel = ? WHERE Dni = ?", (nom, apll, mail, pwd, tel, dni))
    
    conn.commit()
    conn.close()