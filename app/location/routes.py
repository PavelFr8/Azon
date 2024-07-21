@app.route('/address', methods=['GET', 'POST'])
@login_required
def address():
    query = request.args.get('query')
    closest_shops = find_shops(query)
    if closest_shops == 'Некорректные введённые данные':
        return render_template('address.html', title='Выбор адреса', text=query, closest_shops=closest_shops,
                               message='Некорректные введённые данные')
    return render_template('address.html', title='Выбор адреса', text=query, closest_shops=closest_shops)


@app.route('/choose_address/<address>')
@login_required
def choose_address(address):
    db_sess = get_db_session()
    user: User = db_sess.query(User).get(current_user.id)
    if user:
        user.address = address
        db_sess.commit()
    return redirect('/buy')