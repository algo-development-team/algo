from flask import Blueprint, request, jsonify

bp = Blueprint('/api/user', __name__, url_prefix='/api/user')

# algorithm:
# preferred type = 100
# non-preferred type = 1
# example:
# original: [90, 70, 30]
# preferred type -> 2
# updated: [1, 100, 1]
def get_rankings_3d_matrix_extreme(
  rankings,
  rankings_ww_user_specified,
  rankings_pw_user_specified,
  rankings_pnw_user_specified
  ):
  rankings_3d_matrix = [[rankings['urgent_rankings_ww'], rankings['deep_rankings_ww'], rankings['shallow_rankings_ww']], 
                        [rankings['urgent_rankings_pw'], rankings['deep_rankings_pw'], rankings['shallow_rankings_pw']], 
                        [rankings['urgent_rankings_pnw'], rankings['deep_rankings_pnw'], rankings['shallow_rankings_pnw']]]
  rankings_matrix_user_specified = [rankings_ww_user_specified,
                                    rankings_pw_user_specified,
                                    rankings_pnw_user_specified]

  for i in range(len(rankings_matrix_user_specified)):
    for j in range(len(rankings_matrix_user_specified[i])):
      # ranking_type is the index of the preferred type in type_rankings
      ranking_type = rankings_matrix_user_specified[i][j] - 1

      # user has requested change in the rankings
      if ranking_type != -1:

        # type_rankings is the list of verticle slice of rankings_matrix_(ww or pw or pnw) at index j, excluding the ranking_type index within the verticle slice
        # type_rankings: two elements out of [rankings_3d_matrix[i][0][j], rankings_3d_matrix[i][1][j], rankings_3d_matrix[i][2][j]]  
        type_rankings_indexes = [0, 1, 2]
        type_rankings_indexes.remove(ranking_type)
        type_rankings = [rankings_3d_matrix[i][type_rankings_indexes[0]][j], rankings_3d_matrix[i][type_rankings_indexes[1]][j]]

        # rankings_3d_matrix value reassignment
        rankings_3d_matrix[i][ranking_type][j] = 100
        rankings_3d_matrix[i][type_rankings_indexes[0]][j] = 1
        rankings_3d_matrix[i][type_rankings_indexes[1]][j] = 1
  return rankings_3d_matrix

@bp.route('/', methods=['GET'])
def get_user():
  from models import User

  data = request.get_json()

  user = User.query.filter_by(email=data['email']).first()
  if user is None:
    return 'User Not Found', 404
  
  return jsonify(user.serialize())

@bp.route('/update', methods=['PATCH'])
def update_user():
  from app import db
  from models import User
  
  data = request.get_json()

  user = User.query.filter_by(email=data['email']).first()
  if user is None:
    return 'User Not Found', 404

  else:
    user.picture = data['picture']
    user.work_time_range = data['work_time_range']
    user.sleep_time_range = data['sleep_time_range']
    user.work_days = data['work_days']
    user.is_setup = True

    db.session.commit()

  return 'User Updated'

# not used in the frontend yet
# modify as needed to fit the future user rankings adjustment system implementation
@bp.route('/update-rankings-development', methods=['PATCH'])
def update_rankings_user():
  from app import db
  from models import User
  
  data = request.get_json()

  user = User.query.filter_by(email=data['email']).first()
  if user is None:
    return 'User Not Found', 404

  else:  
    # passing all the user rankings by value
    # passing by reference will prevent the fields being updated later on
    rankings = user.get_rankings()

    rankings_3d_matrix = get_rankings_3d_matrix_extreme(
      rankings=rankings,
      rankings_ww_user_specified=data['rankings_ww_user_specified'],
      rankings_pw_user_specified=data['rankings_pw_user_specified'],
      rankings_pnw_user_specified=data['rankings_pnw_user_specified']
    )

    # DEBUG
    print('rankings_3d_matrix:')
    for rankings_matrix in rankings_3d_matrix:
      for rankings in rankings_matrix:
        print(rankings)
    
    user.urgent_rankings_ww = rankings_3d_matrix[0][0]
    user.deep_rankings_ww = rankings_3d_matrix[0][1]
    user.shallow_rankings_ww = rankings_3d_matrix[0][2]
    user.urgent_rankings_pw = rankings_3d_matrix[1][0]
    user.deep_rankings_pw = rankings_3d_matrix[1][1]
    user.shallow_rankings_pw = rankings_3d_matrix[1][2]
    user.urgent_rankings_pnw = rankings_3d_matrix[2][0]
    user.deep_rankings_pnw = rankings_3d_matrix[2][1]
    user.shallow_rankings_pnw = rankings_3d_matrix[2][2]

    db.session.commit()

  return 'User Rankings Updated'

@bp.route('/update-checklist', methods=['PATCH'])
def update_checklist_user():
  from app import db
  from models import User
  
  data = request.get_json()

  user = User.query.filter_by(email=data['email']).first()
  if user is None:
    return 'User Not Found', 404

  else:
    user.checklist = data['checklist']
    db.session.commit()  

  return 'Checklist Updated'