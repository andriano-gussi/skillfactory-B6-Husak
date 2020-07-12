from bottle import route, run, HTTPError, request

# импортируем модуль album.py для взаимодействия с базой данных музыкальной библиотеки
import album

# обрабатываем GET-запросы по адресу /albums/<artist>
@route("/albums/<artist>")
def read_albums(artist):
    """ выводит сообщение с количеством альбомов исполнителя artist и списком названий этих альбомов """
    
    # делаем заглавными первые буквы параметра artist на тот случай, если пользователь введет данные в нижнем регистре
    artist = artist.title()
    # формируем список альбомов по запрошенному артисту
    albums_list = album.find(artist)
    # если список пуст, выводим соответствующее сообщение об ошибке
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    # иначе выводим данные по альбомам 
    else:
        album_names = [". ".join([str(i+1), album.album]) for i, album in enumerate(albums_list)]
        result = "Количество альбомов {}: {}{}".format(artist, len(albums_list), "<br><br>")
        result += "<br>".join(album_names)
    return result

# обрабатываем POST-запросы по адресу /albums/
@route("/albums", method="POST")
def create_new_artist():
    """ сохраняет в базу данных переданную пользователем информацию о новом альбоме """
    class MinError(Exception):
        """ вспомагательный пустой класс для обработки пользовательского исключения """
        pass

    # вспомагательная переменная (если в базе данных обнаружится существующая запись - изменим на True) 
    exist = False

    try:
        # из переданных в веб-формате данных о новом альбоме формируем новую строку для записи в базу
        # создаем экземпляр класса Album() из модуля "album.py"
        artist_data = album.Album(
            year=int(request.forms.get("year")),
            artist=request.forms.get("artist"),
            genre=request.forms.get("genre"),
            album=request.forms.get("album")
            )
        # если указанный год альбома меньше 1860 года (т.е. когда была создана первая в мире аудиозапись),
        # возбуждаем соответствующее исключение
        if artist_data.year < 1860:
            raise MinError()
        
        # формируем список альбомов по запрошенному артисту
        albums_list = album.find(artist_data.artist)
        # сверяем данные нового альбома с существующими альбомами артиста
        for item in albums_list:
            if artist_data == item:
                return HTTPError(409, "Такая запись в базе данных уже есть!")
                exist = True
                break

        # если такого альбома нет - сохраняем в базу данных новый альбом
        if not exist:
            album.save(artist_data)
            return "Данные успешно сохранены!"

    # перехватываем ошибку, когда пользователь ввел не целое число в year
    except ValueError:
        return "Некорректно указан год!"
    # перехватываем, когда введен год, меньше 1860г
    except MinError:
        return "Указанный год меньше 1860г!(в этом году была осуществлена самая первая аудиозапись в мире!)"

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)