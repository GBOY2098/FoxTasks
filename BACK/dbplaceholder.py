# Это временная затычка для получения данных
# Я делал по этому гайду: https://www.youtube.com/watch?v=Crxq-d9t_uc (создание бд) и https://www.youtube.com/watch?v=24vVFtwuBWs (привязка ее к авторизации)

class FDataBase:
    def __init__(self):
        pass

    def getUser(self, user_id):
        return {'name': 'Дмитрий', 'surname': 'Суперский', 'class': '10И', 'new_works': [], 'completed_works': [], 'in_progress_works': []}
        # Здесь должен быть запрос по таблице с пользователями с селектом по user_id (это юзернейм)
        # !Данные (наверное) должны приходить именно в таком виде, именно в словаре!