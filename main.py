from flask import Flask, jsonify,  render_template
from flask import request
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import SessionLocal, Movie, Cinema, Hall, Session, Customer, Ticket

# Создаем сессию для взаимодействия с базой данных
db = SessionLocal()

# Создаем экземпляр объекта приложения Flask
app = Flask('gg')


def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


@app.route ('/cinema/show/all', methods = ['GET'])
def getAllCinemas():
    with SessionLocal() as db:
        cinemas = db.query(Cinema).all()
        cinemas_dict = [to_dict(cinema) for cinema in cinemas]
    return render_template('cinemas.html', cinemas=cinemas_dict)

@app.route ('/cinema/show/all/json', methods = ['GET'])
def getAllCinemasJson():
    with SessionLocal() as db:
        cinemas = db.query(Cinema).all()
        cinemas_dict = [to_dict(cinema) for cinema in cinemas]
    return jsonify(cinemas_dict),200


@app.route("/cinema/add", methods=['POST'])
def cinema_add():
    data = request.json
    new_cinema = Cinema(name=data['name'], address=data['address'])

    with SessionLocal() as db:
        db.add(new_cinema)
        db.commit()  # Commit within the session scope

        # Access id attribute after committing within session scope
        return jsonify({
            "status": "Cinema added successfully",
            "id": new_cinema.cinema_id
        }), 200


@app.route ('/cinema/show/<int:cinema_id>', methods = ['GET'])
def getCinemaById(cinema_id):
    with SessionLocal() as db:
        cinemas = db.query(Cinema).get(cinema_id)
        if cinemas:
            cinemas_dict = to_dict(cinemas)
            return jsonify(cinemas_dict)
        else:
            return jsonify({"error": "Cinema not found"}), 404


@app.route ('/cinema/delete/<int:cinema_id>', methods = ['DELETE'])
def deleteCinemaById(cinema_id):
    with SessionLocal() as db:
        cinema = db.query(Cinema).get(cinema_id)
        if cinema is not None:
            db.delete(cinema)
            db.commit()
            return jsonify({'status': 'Успешно удалено'}), 200
        else:
            return jsonify({"error": "Кинотеатр не найден"}), 404


@app.route('/cinema/update/<int:cinema_id>', methods=['PUT'])
def updateCinemaById(cinema_id):
    # Получаем данные для обновления из тела запроса в формате JSON
    data = request.json
    with SessionLocal() as db:
        cinema = db.query(Cinema).get(cinema_id)
        if cinema is not None:  # Проверяем, существует ли кинотеатр
            # Обновляем имя кинотеатра, если оно есть в данных запроса
            if 'name' in data:
                cinema.name = data['name']
            # Обновляем адрес кинотеатра, если он есть в данных запроса
            if 'address' in data:
                cinema.address = data['address']
            db.commit()  # Фиксируем изменения в базе данных
            cinema_dict = to_dict(cinema)
            return jsonify({'status': 'Данные успешно обновлены', 'cinema': cinema_dict}), 200
        else:
            return jsonify({"error": "Кинотеатр не найден"}), 404


@app.route('/movies/show/all', methods=['GET'])
def getAllMovies():
    with SessionLocal() as db:
        movies = db.query(Movie).all()
        movies_dict = [to_dict(movie) for movie in movies]
    return render_template('movies.html', movies=movies_dict)\


@app.route('/movies/show/all/json', methods=['GET'])
def getAllMoviesJson():
    with SessionLocal() as db:
        movies = db.query(Movie).all()
        movies_dict = [to_dict(movie) for movie in movies]
    return jsonify(movies_dict),200

@app.route('/movies/show/<int:movie_id>', methods=['GET'])
def getMovieById(movie_id):
    with SessionLocal() as db:
        movie = db.query(Movie).get(movie_id)
        if movie:
            movie_dict = to_dict(movie)
            return jsonify(movie_dict)
        else:
            return jsonify({"error": "Movie not found"}), 404

@app.route('/movies/delete/<int:movie_id>', methods=['DELETE'])
def deleteMovieById(movie_id):
    with SessionLocal() as db:
        movie = db.query(Movie).get(movie_id)
        if movie:
            db.delete(movie)
            db.commit()
            return jsonify({'status': 'Успешно удалено'}), 200
        else:
            return jsonify({"error": "Movie not found"}), 404

@app.route('/movies/update/<int:movie_id>', methods=['PUT'])
def updateMovieById(movie_id):
    data = request.json
    with SessionLocal() as db:
        movie = db.query(Movie).get(movie_id)
        if movie:
            if 'title' in data:
                movie.title = data['title']
            if 'description' in data:
                movie.description = data['description']
            if 'genre' in data:
                movie.genre = data['genre']
            if 'director' in data:
                movie.director = data['director']
            if 'actors' in data:
                movie.actors = data['actors']
            db.commit()
            movie_dict = to_dict(movie)
            return jsonify({'status': 'Данные успешно обновлены', 'movie': movie_dict}), 200
        else:
            return jsonify({"error": "Movie not found"}), 404


# Функция для отображения всех залов
@app.route('/halls/show/all', methods=['GET'])
def getAllHalls():
    with SessionLocal() as db:
        halls = db.query(Hall).all()
        halls_dict = [to_dict(hall) for hall in halls]
    return render_template('halls.html', halls=halls_dict)

# Функция для отображения зала по ID
@app.route('/halls/show/<int:hall_id>', methods=['GET'])
def getHallById(hall_id):
    with SessionLocal() as db:
        hall = db.query(Hall).get(hall_id)
        if hall:
            hall_dict = to_dict(hall)
            return jsonify(hall_dict)
        else:
            return jsonify({"error": "Hall not found"}), 404

# Функция для удаления зала по ID
@app.route('/halls/delete/<int:hall_id>', methods=['DELETE'])
def deleteHallById(hall_id):
    with SessionLocal() as db:
        hall = db.query(Hall).get(hall_id)
        if hall:
            db.delete(hall)
            db.commit()
            return jsonify({'status': 'Успешно удалено'}), 200
        else:
            return jsonify({"error": "Hall not found"}), 404

# Функция для обновления зала по ID
@app.route('/halls/update/<int:hall_id>', methods=['PUT'])
def updateHallById(hall_id):
    data = request.json
    with SessionLocal() as db:
        hall = db.query(Hall).get(hall_id)
        if hall:
            if 'name' in data:
                hall.name = data['name']
            if 'cinema_id' in data:
                hall.cinema_id = data['cinema_id']
            if 'capacity' in data:
                hall.capacity = data['capacity']
            db.commit()
            hall_dict = to_dict(hall)
            return jsonify({'status': 'Данные успешно обновлены', 'hall': hall_dict}), 200
        else:
            return jsonify({"error": "Hall not found"}), 404


# Функция для отображения всех сеансов
@app.route('/sessions/show/all', methods=['GET'])
def getAllSessions():
    with SessionLocal() as db:
        sessions = db.query(Session).all()
        sessions_dict = [to_dict(session) for session in sessions]
    return render_template('sessions.html', sessions=sessions_dict)

# Функция для отображения сеанса по ID
@app.route('/sessions/show/<int:session_id>', methods=['GET'])
def getSessionById(session_id):
    with SessionLocal() as db:
        session = db.query(Session).get(session_id)
        if session:
            session_dict = to_dict(session)
            return jsonify(session_dict)
        else:
            return jsonify({"error": "Session not found"}), 404

# Функция для удаления сеанса по ID
@app.route('/sessions/delete/<int:session_id>', methods=['DELETE'])
def deleteSessionById(session_id):
    with SessionLocal() as db:
        session = db.query(Session).get(session_id)
        if session:
            db.delete(session)
            db.commit()
            return jsonify({'status': 'Успешно удалено'}), 200
        else:
            return jsonify({"error": "Session not found"}), 404

# Функция для обновления сеанса по ID
@app.route('/sessions/update/<int:session_id>', methods=['PUT'])
def updateSessionById(session_id):
    data = request.json
    with SessionLocal() as db:
        session = db.query(Session).get(session_id)
        if session:
            if 'movie_id' in data:
                session.movie_id = data['movie_id']
            if 'hall_id' in data:
                session.hall_id = data['hall_id']
            if 'start_time' in data:
                session.start_time = data['start_time']
            if 'end_time' in data:
                session.end_time = data['end_time']
            if 'price' in data:
                session.price = data['price']
            db.commit()
            session_dict = to_dict(session)
            return jsonify({'status': 'Данные успешно обновлены', 'session': session_dict}), 200
        else:
            return jsonify({"error": "Session not found"}), 404


# Функция для отображения всех клиентов
@app.route('/customers/show/all', methods=['GET'])
def getAllCustomers():
    with SessionLocal() as db:
        customers = db.query(Customer).all()
        customers_dict = [to_dict(customer) for customer in customers]
    return render_template('customers.html', customers=customers_dict)

# Функция для отображения клиента по ID
@app.route('/customers/show/<int:customer_id>', methods=['GET'])
def getCustomerById(customer_id):
    with SessionLocal() as db:
        customer = db.query(Customer).get(customer_id)
        if customer:
            customer_dict = to_dict(customer)
            return jsonify(customer_dict)
        else:
            return jsonify({"error": "Customer not found"}), 404

# Функция для удаления клиента по ID
@app.route('/customers/delete/<int:customer_id>', methods=['DELETE'])
def deleteCustomerById(customer_id):
    with SessionLocal() as db:
        customer = db.query(Customer).get(customer_id)
        if customer:
            db.delete(customer)
            db.commit()
            return jsonify({'status': 'Успешно удалено'}), 200
        else:
            return jsonify({"error": "Customer not found"}), 404

# Функция для обновления клиента по ID
@app.route('/customers/update/<int:customer_id>', methods=['PUT'])
def updateCustomerById(customer_id):
    data = request.json
    with SessionLocal() as db:
        customer = db.query(Customer).get(customer_id)
        if customer:
            if 'full_name' in data:
                customer.full_name = data['full_name']
            if 'phone' in data:
                customer.phone = data['phone']
            if 'email' in data:
                customer.email = data['email']
            db.commit()
            customer_dict = to_dict(customer)
            return jsonify({'status': 'Данные успешно обновлены', 'customer': customer_dict}), 200
        else:
            return jsonify({"error": "Customer not found"}), 404


# Функция для отображения всех билетов
@app.route('/tickets/show/all', methods=['GET'])
def getAllTickets():
    with SessionLocal() as db:
        tickets = db.query(Ticket).all()
        tickets_dict = [to_dict(ticket) for ticket in tickets]
    return render_template('tickets.html', tickets=tickets_dict)

# Функция для отображения билета по ID
@app.route('/tickets/show/<int:ticket_id>', methods=['GET'])
def getTicketById(ticket_id):
    with SessionLocal() as db:
        ticket = db.query(Ticket).get(ticket_id)
        if ticket:
            ticket_dict = to_dict(ticket)
            return jsonify(ticket_dict)
        else:
            return jsonify({"error": "Ticket not found"}), 404

# Функция для удаления билета по ID
@app.route('/tickets/delete/<int:ticket_id>', methods=['DELETE'])
def deleteTicketById(ticket_id):
    with SessionLocal() as db:
        ticket = db.query(Ticket).get(ticket_id)
        if ticket:
            db.delete(ticket)
            db.commit()
            return jsonify({'status': 'Успешно удалено'}), 200
        else:
            return jsonify({"error": "Ticket not found"}), 404

# Функция для обновления билета по ID
@app.route('/tickets/update/<int:ticket_id>', methods=['PUT'])
def updateTicketById(ticket_id):
    data = request.json
    with SessionLocal() as db:
        ticket = db.query(Ticket).get(ticket_id)
        if ticket:
            if 'session_id' in data:
                ticket.session_id = data['session_id']
            if 'customer_id' in data:
                ticket.customer_id = data['customer_id']
            if 'seat_number' in data:
                ticket.seat_number = data['seat_number']
            if 'price' in data:
                ticket.price = data['price']
            db.commit()
            ticket_dict = to_dict(ticket)
            return jsonify({'status': 'Данные успешно обновлены', 'ticket': ticket_dict}), 200
        else:
            return jsonify({"error": "Ticket not found"}), 404


@app.route('/stats/purchases', methods=['GET'])
def getPurchaseStats():
    with SessionLocal() as db:
        # Получаем общее количество билетов
        total_tickets = db.query(func.sum(Ticket.seat_number)).scalar()

        # Получаем общую сумму продаж
        total_revenue = db.query(func.sum(Ticket.price)).scalar()

        # Получаем среднюю стоимость билета
        average_price = db.query(func.avg(Ticket.price)).scalar()

    # Формируем словарь с результатами
    stats = {
        'total_tickets': total_tickets or 0,  # Если нет данных, возвращаем 0
        'total_revenue': total_revenue or 0.0,  # Если нет данных, возвращаем 0.0
        'average_price': average_price or 0.0,  # Если нет данных, возвращаем 0.0
    }

    return jsonify(stats)


@app.route('/stats/cinema', methods= ['GET'])
def statss():
    return render_template('stats_cinema.html')

@app.route('/stats/movies', methods= ['GET'])
def statss_movies():
    return render_template('stats_movies.html')


@app.route('/statistics/cinemas', methods=['GET'])
def get_cinemas_statistics():
    with SessionLocal() as db:
        # Получаем количество залов в каждом кинотеатре
        cinemas = db.query(Cinema).all()
        cinemas_statistics = []

        for cinema in cinemas:
            halls_count = db.query(Hall).filter(Hall.cinema_id == cinema.cinema_id).count()
            sessions_count = db.query(Session).join(Hall).filter(Hall.cinema_id == cinema.cinema_id).count()

            cinemas_statistics.append({
                'cinema_id': cinema.cinema_id,
                'name': cinema.name,
                'address': cinema.address,
                'halls_count': halls_count,
                'sessions_count': sessions_count
            })

    return jsonify(cinemas_statistics)


@app.route('/statistics/movies', methods=['GET'])
def get_movies_statistics():
    with SessionLocal() as db:
        # Получаем количество сеансов для каждого фильма
        movies = db.query(Movie).all()
        movies_statistics = []

        for movie in movies:
            sessions_count = db.query(Session).filter(Session.movie_id == movie.movie_id).count()

            movies_statistics.append({
                'movie_id': movie.movie_id,
                'title': movie.title,
                'sessions_count': sessions_count
            })

    return jsonify(movies_statistics)



# Если файл запускается напрямую, а не импортируется
if __name__ == '__main__':
    # Запускаем веб-сервер Flask
    app.run(debug=True, port=8080)
