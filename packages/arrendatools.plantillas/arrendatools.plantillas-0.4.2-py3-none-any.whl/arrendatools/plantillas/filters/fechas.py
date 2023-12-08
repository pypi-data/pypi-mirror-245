import calendar
import pytz
from datetime import datetime, timedelta
from babel.dates import format_datetime, get_timezone


def dias_del_año(año):
    """
    Calcula los dias que tiene un año teniendo en cuenta si es bisiesto o no

    Args:
        año (int): Año para calcular los dias.

    Returns:
        int: Numero de dias del año indicado
    """

    if calendar.isleap(año):
        return 366
    else:
        return 365


def formato_fecha(fecha_hora=None, formato='medium', tzinfo='Europe/Madrid', locale='es_ES'):
    """
    Convierte una fecha dada en formato ISO8601 al formato especificado. Ver https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

    Args:

        fecha_hora (str): fecha en formato ISO8601. Si no se pasa ninguna se usa la fecha y hora actual
        formato (str): uno de  “full”, “long”, “medium”, o “short”, o un patron datetime personalizado. "medium" por defecto.
        tzinfo (str): la zona horaria a aplicar para dar formato a la fecha-hora. "Europe/Madrid" por defecto.
        locale (str): identificador de locale. es_ES por defecto.

    Returns:
        str: La fecha en texto con el formato indicado
    """
    date = None
    time_zone = get_timezone(tzinfo)
    if isinstance(fecha_hora, str):
        date = datetime.fromisoformat(fecha_hora)

    return format_datetime(date, formato, time_zone, locale)


def aplicar_timedelta(fecha, semanas=0, dias=0, horas=0, minutos=0, segundos=0):
    """
    Aplica un delta a una fecha proporcionada.

    Args:

        fecha (str): fecha en formato ISO8601.
        semanas (int): Numero de semanas a aplicar. Positivo para sumar, negativo para restar.
        dias (int): Numero de días a aplicar. Positivo para sumar, negativo para restar.
        horas (int): Numero de horas a aplicar. Positivo para sumar, negativo para restar.
        minutos (int): Numero de minutos a aplicar. Positivo para sumar, negativo para restar.
        segundos (int): Numero de segundos a aplicar. Positivo para sumar, negativo para restar.

    Returns:
        str: La fecha con el delta aplicado en formato ISO8601.
    """
    fecha_obj = datetime.fromisoformat(fecha)
    delta = timedelta(days=dias, hours=horas, minutes=minutos, seconds=segundos, weeks=semanas)
    nueva_fecha = fecha_obj + delta
    return nueva_fecha.isoformat()


def trimestre(fecha, delta=0):
    """
    Calcula el trimestre de la fecha indicada. Se le puede pasar un delta positivo o negativo para añadir o eliminar trimestres enteros a la fecha.
    Lo devuelve en el formato '<trimeste>T <año>'

    Args:

        fecha (str): fecha en formato ISO8601.
        delta (int): Numero de trimestres a sumar a la fecha. Positivo para sumar, negativo para restar.

    Returns:
        str: Trimestre de la fecha indicada con el formato '<trimeste>T <año>'.
    """
    fecha_trimestre = aplicar_timedelta(fecha, dias=delta * 30 * 3)
    fecha_obj = datetime.fromisoformat(fecha_trimestre)
    num_trimestre = (fecha_obj.month - 1) // 3 + 1
    return str(num_trimestre) + 'T ' + str(fecha_obj.year)


def dias_entre(fecha_inicio, fecha_fin, formato_inicio='%Y-%m-%dT%H:%M:%S.%fZ', formato_fin='%Y-%m-%dT%H:%M:%S.%fZ', tzinfo_inicio='Europe/Madrid', tzinfo_fin='Europe/Madrid'):
    """
    Calcula los dias enteros transcurridos entre 2 fechas.
    Sólo cuenta días enteros, esto significa que si se quiere contar el día final hay que sumar 1 día a la fecha final.
    Si las fechas contienen la hora (con zona horaria) esta se convierte a UTC.
    Por ejemplo:
        fecha_incio: 2023-12-01
        fecha_fin: 2023-12-31.
        Devuelve 30, por lo que para tener en cuenta el día 31/12 hay que usar como fecha fin 2024-01-01.

    Args:

        fecha_inicio (str): fecha inicial.
        fecha_fin (str): fecha final.
        formato_inicio (str) Formato para parsear la fecha inicio. Por defecto: '%Y-%m-%dT%H:%M:%S.%fZ'
        formato_fin (str) Formato para parsear la fecha fin. Por defecto: '%Y-%m-%dT%H:%M:%S.%fZ'
        tzinfo_inicio (str) Zona horaria del string pasado para la fecha inicial. Por defecto: Europe/Madrid
        tzinfo_fin (str) Zona horaria del string pasado para la fecha inicial. Por defecto: Europe/Madrid

    Returns:
        int: Número de días enteros que han transcurrido entre las 2 fechas.
    """
    zona_inicio = pytz.timezone(tzinfo_inicio)
    zona_fin = pytz.timezone(tzinfo_fin)
    fecha_inicio_obj = zona_inicio.localize(datetime.strptime(fecha_inicio, formato_inicio))
    fecha_fin_obj = zona_fin.localize(datetime.strptime(fecha_fin, formato_fin))
    diferencia = fecha_fin_obj - fecha_inicio_obj
    return diferencia.days
