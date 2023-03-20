import sys
import argparse
import csv
import os
import time
import requests

# input: archivo de entrada con las ips a analizar
# historico: archivo con las ips analizadas previamente

# all_ips: variable input procesada (csv a array)
# ips_unique: listado de ips (all_ips) unicas (sin repetir), toma como input all_ips
# unrated_ips: ips que no están en el historico, toma como input unique_ips
# analyze_ips: ips a analizar que no esten en el historico, toma como input unrated_ips

# Si el historico tiene mas de 6 meses archivar y generar uno nuevo

def countdown(t):
    
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print("Delay: ",timer, end="\r")
        time.sleep(1)
        t -= 1



def parsear_csv(csv_file: str) -> list:
    """Lee un archivo CSV y devuelve una lista de diccionarios con el contenido de cada fila."""
    lst = []
    """Verifico si el archivo existe y proceso"""
    if csv_file and os.path.exists(csv_file):
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            lst = [dct for dct in reader]

    else:
        print("El archivo mencionado en el parámetro no existe")
    
    return lst


def get_unique_ips(ips: list) -> list:
    """Genera una lista de diccionarios con estadísticas de IPs,
    con formato {"addr": "127.0.0.1", "sid": 1, "count": 1}
    Las IPs son únicas y están ordenadas por cantidad de ocurrencias.
    """
    #que hacemos con las reglas que contienen ANY en el addr?? AGUSTIN
    ips_sorted = [dct for dct in ips if dct["sid"] == "any"]
    ips_sorted.sort(key=lambda x: int(x["count"]), reverse=True)

    ips_unique = [ips_sorted[0]]
    for i in range(1, len(ips_sorted)):
        if ips_sorted[i - 1] != ips_sorted[i]:
            ips_unique.append(ips_sorted[i])
        else:
            ips_unique[-1]["count"] += ips_sorted[i]["count"]

    return ips_unique


# merge de get_non_excepted_ips and get_unrated_ips
def deputate_ips(ips: list, filtro: list) -> list:
    """depurar ips"""
    # lista plana de strings con las IPs ya evaluadas
    ips_analyzed = [dct["addr"] for dct in filtro]

    #ips_rated = [dct for dct in ips if dct["addr"] in rated_ip_list]
    depurate_ips = [dct for dct in ips if dct["addr"] not in ips_analyzed]

    return depurate_ips

#def get_non_excepted_ips(ips:list, excepciones:list):
   # pass


def get_ip_reputation(ip: str) -> dict:
    """Realiza una consulta a la API de VirusTotal de la reputación de la IP ingresada.
    """
    try:
        url = "https://www.virustotal.com/api/v3/ip_addresses/"
        headers = { "x-apikey" : "INSERT API KEY" }        ##<<<<----- 
        response = requests.get(url + ip, headers=headers)
        analysis = response.json()["data"]["attributes"]["last_analysis_stats"]
        analysis["addr"] = ip
        #print("analysis:\n" + str(analysis) + "\n")
        return analysis
    
    except:
        sys.exit("\nPor favor revisar conexión con virustotal..\n")


def is_malisious (ip: dict):
    if(int(ip["malicious"]) != 0 or int(ip["suspicious"]) != 0):
        print("La ip: "+ip["addr"]+" es MALICIOSA, revisar!!")

    else:
        print("La ip: "+ip["addr"]+ " no es maliciosa\n")
    
    return int(ip["malicious"]) != 0 or int(ip["suspicious"]) != 0



def write_file(NombreArchivo, header, resultado: dict):
    if (os.path.exists(NombreArchivo)):
        #print ("El archivo existe, se omite creación")
        with open (file=NombreArchivo, mode='a+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header,lineterminator="\n")
            writer.writerow(resultado)
    else:
        #print ("Creando archivo")
        with open (file=NombreArchivo, mode='w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header, lineterminator="\n")
            #print(header) # imprime correctamente el header
            writer.writeheader() # Escribe el header pero no realiza un append
            writer.writerow(resultado)

#######################################################################
### reprocesar historico ###

def reprocesar_historico():
    pass


############################ Bloque principal #########################

                            #### MAIN ####

def main (input: str, historico: str, excepciones: str, delay: int):
    NombreArchivo = "Reputation-analysis-ips_" + time.strftime("%d-%m-%Y-(%H%M%S)") + ".csv"
    header = ("addr", "harmless", "malicious", "suspicious", "undetected", "timeout")
    IpsMaliciosas = "IpsMaliciosas_analisis_" + time.strftime("%d-%m-%Y-(%H%M%S)") + ".csv"
    
    """Booleano que me identifica si el csv (output de analisis_snort) está vacío, sino almaceno el output"""
    # podria ser procesado todo dentro de la función parsear_csv
    if (len(parsear_csv(input)) == 0):
        sys.exit("El archivo a procesar está vacío")
    else:
        all_ips = parsear_csv(input)
        v_historico = parsear_csv(historico)
        v_excepciones = parsear_csv(excepciones)
    
    #print("\nel hostorico es: \n\n")
    #print(historico)

    # verificar que el historico tenga un header

    file = open(file=historico,mode="r")
    lines =file.readlines()

    primera_linea=lines[0].strip()
    if (primera_linea==",".join(header)):
        pass
    else:
        with open (file=historico, mode='w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header, lineterminator="\n")
            #print(header) # imprime correctamente el header
            writer.writeheader() # Escribe el header pero no realiza un append
    


    """obtener ips unicas"""
    unique_ips = get_unique_ips(all_ips)
    #analyze_ips = get_non_excepted_ips(analyze_ips, excepciones)
    """Obtener unicamente ips no analizadas previamente"""
    analyze_ips = deputate_ips(unique_ips, v_historico)
    """Obtener ips no exceptuadas"""
    analyze_ips = deputate_ips(analyze_ips, v_excepciones)
    """Comprobar si tengo ips a analizar posterior a la comparacion con el historico"""
    # Sí luego de comparar con el historico me queda ips por analizar procedo.
    

   # modificar, recorrer todo el array exceptuando la primera linea, first_ip = analize_ips[0], si es que no está vacío
   # Sí luego de comparar con el historico me queda ips por analizar procedo.
    if (len(analyze_ips)>0):
        """"Generar archivo donde volcar el analisis (si y solo si tengo ips a analizar)"""

        only_ips = [dct["addr"] for dct in analyze_ips]
        print ("Enviar a virustotal: ", only_ips[0]  +"\n")
        temporal = get_ip_reputation(only_ips[0])
        print (temporal, "\n")
        write_file(historico,header, temporal)
        # incorporar un timestamp al historico para el reprocesado (fecha numerica *buscar*) utc
        # date '+%s' && echo $EPOCHSECONDS
        
        write_file (NombreArchivo, header, temporal)

        
        if is_malisious(temporal) == True:
            #no hacer nada
            pass
        else:
            # acá incorporar el envio de mails para ips maliciosas
            pass

        #write_file (NombreArchivo, header, get_ip_reputation(only_ips[0]))
        #write_file (NombreArchivo, header, get_ip_reputation(only_ips[0]))
        countdown (int(delay))

        for i in range(1, len(analyze_ips)):
            #print("Comienzo de for")
            #print (i," - ",analyze_ips[i])
            print ("Enviar a virustotal: ",only_ips[i] + "\n")
            # variable temporal para almacenar el resultado mientras de escribe en los registros
            temporal = get_ip_reputation(only_ips[i])
            print (temporal, "\n")
            write_file(historico, header, temporal)
            write_file (NombreArchivo, header, temporal)
            if is_malisious(temporal) == True:
                write_file (IpsMaliciosas, header, temporal)
                
            countdown (int(delay))


            

    ### Para depuración

    #print("\nBloque de depuracion: \n")
    #print("El archivo a procesar es: ",input)
    #print ("Todas las ips a procesar: ", all_ips, "\n", "Histórico: ", historico, "\n")
    #print ("ips unicas", unique_ips) 
    #print ("\n","Enviar a analizar: \n", analyze_ips[1])


## ejecucion principal ##
if __name__=="__main__":
        """Definir objeto parser"""
        parseador = argparse.ArgumentParser("Entrada", description="Archivo de entrada para analisar y el historico de las ips analizadas")

        """Definir argumentos"""
        parseador.add_argument("-i", "--input", required=True)
        parseador.add_argument("-j", "--historico", required=True)
        parseador.add_argument("-e", "--excepciones", required=True)
        parseador.add_argument("-d", "--delay", required=False, default=15)
        """Objeto con el parametro"""
        args = parseador.parse_args()

        """Envio argumentos al mail para ser procesados"""
        main(args.input, args.historico, args.excepciones, args.delay)

else:
    print("El Bloque principal no se ejecuta dado que se llamó al bloque principal como funcion")
















