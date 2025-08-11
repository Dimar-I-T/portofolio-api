from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

def skill_view(request):
    id = request.GET.get('id')
    print("INI SKILLS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!: id: ", id)

    with connection.cursor() as cursor:
        cursor.execute(
            '''
            select s_id, judul, logo, deskripsi
            from main_skills
            where s_id = %s
            ''', [id]
        )

        hasil = cursor.fetchone()
        print(hasil)
        
    if hasil is None:
        return JsonResponse({"success": False, "message": "Tidak ada data"}, status=404)

    return JsonResponse({
        "success": True,
        "message": "Berhasil query!",
        "data": {
            "s_id": hasil[0],
            "judul": hasil[1],
            "logo": hasil[2],
            "deskripsi": hasil[3]
        }
    })

def skill_tools_view(request):
    if request.method == 'GET':
        id = request.GET.get('id')

        with connection.cursor() as cursor:
            cursor.execute(
                '''
                select id, s_judul, s_logo
                from tools
                where s_id = %s
                order by id
                ''', [id]
            )

            hasil = cursor.fetchall() # list of tuples [(id, s_judul, s_logo), (id1, s_judul1, s_logo1), ...]
        
        hasilJson = []
        for row in hasil:
            # row = (id, s_judul, s_logo)
            json = {
                "id": row[0],
                "s_judul": row[1],
                "s_logo": row[2]
            }

            hasilJson.append(json)

        if hasil is None:
            return JsonResponse({"success": False, "message": "Gagal query!"}, status=400)
        
        return JsonResponse({"success": True, "data": hasilJson})
    
def links_view(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        hasilJson = []
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                select id, tujuan, l_logo, l_judul, keterangan
                from links
                where s_id = %s
                order by id
                ''', [id]
            )

            hasil = cursor.fetchall()

        for t in hasil:
            json = {
                'id': t[0],
                'tujuan': t[1],
                'l_logo': t[2],
                'l_judul': t[3],
                'keterangan': t[4]
            }

            hasilJson.append(json)
        
        if hasil is None:
            return JsonResponse({"success": False, "message": "Gagal query!"}, status=400)
        
        return JsonResponse({"success": True, "data": hasilJson})