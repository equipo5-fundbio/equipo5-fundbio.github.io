import sqlite3

def new_patient(dni, nom, apll, mail, pwd, tel, nac, sex, proc, peso, alt, centro, riss, comorb, med, data, treatment):
    conn = sqlite3.connect('TW.db', timeout=10)
    cursor = conn.cursor()
    
    conn.execute("INSERT INTO pacientes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (dni, nom, apll, mail, pwd, tel, nac, sex, proc, peso, alt, centro, riss, comorb, med, data, treatment))
    conn.commit()
    conn.close()

def patient_info(dni):
    conn = sqlite3.connect('TW.db', timeout=10)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM pacientes WHERE Dni = ?", (dni,))
    resultado = cursor.fetchone()
    conn.commit()
    conn.close()
    return resultado
    #si no está registrado resultado = None
    
#introducir los nuevos datos
def edit_patient(dni, nom, apll, mail, pwd, tel, nac, sex, proc, peso, alt, centro, riss, comorb, med, data, treatment):
    conn = sqlite3.connect('TW.db', timeout=10)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE pacientes SET Nom = ?, Apll = ?, Mail = ?, Pwd = ?, Tel = ?, Nac = ?, Sex = ?, Proc= ?, Peso = ?, Alt = ?, Centro = ?,Riss = ?, Comorb = ?, Med = ? , Data = ?, Treatment = ? WHERE Dni = ?", (nom, apll, mail, pwd, tel, nac, sex, proc, peso, alt, centro, riss, comorb, med, data, treatment, dni))
    
    conn.commit()
    conn.close()

def new_medic(dni, nom, apll, mail, pwd, tel):
    conn = sqlite3.connect('TW.db', timeout=10)
    cursor = conn.cursor()
    
    conn.execute("INSERT INTO medicos VALUES (?, ?, ?, ?, ?, ?)", (dni, nom, apll, mail, pwd, tel))
    conn.commit()
    conn.close()
    
def medic_info(dni):
    conn = sqlite3.connect('TW.db', timeout=10)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM medicos WHERE Dni = ?", (dni,))
    resultado = cursor.fetchone()
    conn.commit()
    conn.close()
    return resultado
    
def patients_from_medic(dnidoc):
    conn = sqlite3.connect('TW.db', timeout=10)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM pacientes WHERE Med = ?", (dnidoc,))
    resultado = cursor.fetchall()
    conn.commit()
    conn.close()
    return resultado
    
#introducir los nuevos datos
def edit_medic(dni, nom, apll, mail, pwd, tel):
    conn = sqlite3.connect('TW.db')
    cursor = conn.cursor()
    
    cursor.execute("UPDATE medicos SET Nom = ?, Apll = ?, Mail = ?, Pwd = ?, Tel = ? WHERE Dni = ?", (nom, apll, mail, pwd, tel, dni))
    
    conn.commit()
    conn.close()