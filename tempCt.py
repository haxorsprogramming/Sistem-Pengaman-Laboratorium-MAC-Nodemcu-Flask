import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from flask import Flask, redirect, url_for, render_template, request, jsonify

app = Flask(__name__)

selected = ['Pclass', 'Sex', 'Age', 'Fare', 'family_size', 'family_survival']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/proses', methods = ['POST', 'GET'])
def proses():
    # {'age':age, 'sex':sex, 'siblings':siblings, 'cabin':cabin, 'married':married}
    # phase 1
    train = pd.read_csv('train.csv')
    test = pd.read_csv('test.csv')
    # phase 2
    train['set'], test['set'] = 'train', 'test'
    combined = pd.concat([train, test])
    # phase 3
    # print(combined.isnull().sum())
    pclass = combined.loc[combined.Fare.isnull(), 'Pclass'].values[0]
    median_fare = combined.loc[combined.Pclass== pclass, 'Fare'].median()
    combined.loc[combined.Fare.isnull(), 'Fare'] = median_fare
    combined['Title'] = combined['Name'].str.extract('([A-Za-z]+)\.', expand=True)
    title_reduction = {'Mr': 'Mr', 'Mrs': 'Mrs', 'Miss': 'Miss', 
                   'Master': 'Master', 'Don': 'Mr', 'Rev': 'Rev',
                   'Dr': 'Dr', 'Mme': 'Miss', 'Ms': 'Miss',
                   'Major': 'Mr', 'Lady': 'Mrs', 'Sir': 'Mr',
                   'Mlle': 'Miss', 'Col': 'Mr', 'Capt': 'Mr',
                   'Countess': 'Mrs','Jonkheer': 'Mr',
                   'Dona': 'Mrs'}
    combined['Title'] = combined['Title'].map(title_reduction)
    for title, age in combined.groupby('Title')['Age'].median().iteritems():
        # print(title, age)
        combined.loc[(combined['Title']==title) & (combined['Age'].isnull()), 'Age'] = age

    combined['surname'] = combined['Name'].apply(lambda x: x.split(",")[0])
    combined = combined.groupby(['surname', 'Fare']).apply(other_family_members_survived).reset_index(drop=True)


    combined = combined.groupby(['Ticket']).apply(lambda x: other_family_members_survived(x, label='family_survival_ticket')).reset_index(drop=True)
    combined.loc[combined['family_survival'] == 0.5, 'family_survival'] = combined.loc[combined['family_survival'] == 0.5, 'family_survival_ticket']

    #Dapatkan ukuran keluarga dari Parch dan Sibsp
    combined['family_size'] = combined['Parch'] + combined['SibSp']

    #Convert feature to number
    combined['Sex'] = LabelEncoder().fit_transform(combined['Sex'])

    combined.loc[:, 'Age'] = pd.qcut(combined['Age'], 4, labels=False)
    combined.loc[:, 'Fare'] = pd.qcut(combined['Fare'], 5, labels=False)

    #Pilih hanya kolom yang akan kita gunakan dan skalakan
    
    scaler  = StandardScaler()
    scaler.fit(combined[selected])
    combined[selected] = scaler.transform(combined[selected])

    combined.to_parquet('titanic_family_survivabillity.parquet', index=False)

    train = combined.loc[combined['set'] == 'train'].drop('set', axis=1).reset_index(drop=True)
    test = combined.loc[combined['set'] == 'test'].drop(['set', 'Survived'], axis=1).reset_index(drop=True)

   

    # test function
    vec1 = np.array([3, 0])
    vec2 = np.array([0, 4])

    # this is the 3:4:5 triangle and therefore, it should return 5 (Long live Pythagoras)
    euclidean_distance(vec1, vec2)

    # test function
    vec1 = np.array([3, 0])
    vec2 = np.array([0, 4])

    # this is the 3:4:5 triangle and therefore, it should return 5 (Long live Pythagoras)
    euclidean_distance(vec1, vec2)

    # test function
    dataset = pd.DataFrame([
        {'a': 1, 'b': 1, 'Survived': 1},
        {'a': 2, 'b': 2, 'Survived': 1},
        {'a': 3, 'b': 3, 'Survived': 0},
        {'a': 4, 'b': 4, 'Survived': 0},
        {'a': 5, 'b': 5, 'Survived': 0},
    ])
    vector = pd.Series({'a': 2.5, 'b': 2.5})

    # should be (2,2) and (3,3) (if keeping track of duplicates)
    get_nearest_neighbor(vector, dataset)

    # print(predict(vector, dataset))
    # print(predict(pd.Series({'a': 4.5, 'b': 4.5}), dataset))
    age = request.form['age']
    sex = request.form['sex']
    siblings = request.form['siblings']
    cabin = request.form['cabin']
    married = request.form['married']
    pass_id_temp = 0

    # if int(age) < 20:
    #     pass_id_temp += 20
    # else:
    #     pass_id_temp += 40

    if cabin == 'f':
        pass_id_temp += 7
    elif cabin == 's':
        pass_id_temp += 8
    else:
        pass_id_temp += 9
    
    if married == 'y':
        pass_id_temp += 100
    else:
        pass_id_temp += 200

    final_test = predict_testset(test, train, number_of_neighbors=10)
    result = final_test[['PassengerId', 'Survived']].copy()
    hjson = result.to_numpy()
    hasil = 0
    # print(result)
    # print(pass_id_temp)
    for x in hjson:
        pass_id = x[0]
        if pass_id == pass_id_temp:
            hasil = x[1]
        else:
            hasil = 0

    
    context = {
        'age' : age,
        'sex' : sex,
        'siblings' : siblings,
        'cabin' : cabin,
        'married' : married,
        'hasil' : hasil
    }
    return jsonify(context)


def other_family_members_survived(dataset, label='family_survival'):
    """
    Periksa apakah anggota keluarga lainnya selamat


      -> 0 tidak ada yang selamat
      -> 1 setidaknya satu anggota keluarga lainnya selamat
      -> 0.5 tidak diketahui apakah anggota lain selamat atau seseorang sendirian
    
    """
    ds = dataset.copy()
    if len(dataset) == 1:
        ds[label] = 0.5
        return ds
    result = []
    for ix, row in dataset.iterrows():
        survived_fraction = dataset.drop(ix)['Survived'].mean()
        if np.isnan(survived_fraction):
            result.append(0.5)
        elif survived_fraction == 0:
            result.append(0)
        else:
            result.append(1)
    ds[label] = result
    return ds    

def euclidean_distance(vector1, vector2):
    return np.sqrt(np.sum((vector1 - vector2)**2))

# A first implementation
def get_nearest_neighbor(vector, dataset, number_of_neighbors=1, ignore_cols=['Survived']):
    distances = []
    for ix, row in dataset.loc[:, ~dataset.columns.isin(ignore_cols)].iterrows():
        distance = euclidean_distance(row, vector)
        distances.append((distance, ix))
    indices = [x[1] for x in sorted(distances, key=lambda x: x[0])]
    neighbors = dataset.loc[indices[:number_of_neighbors]]
    return neighbors

# Another implementation using Pandas
def get_nearest_neighbor(vector, dataset, number_of_vectors=1, ignore_cols=['Survived'], not_count_duplicates=False):
    ds = dataset.copy()
    ds['distance'] = ds.loc[:, ~ds.columns.isin(ignore_cols)].apply(
        lambda x: euclidean_distance(x, vector), axis=1)
    if not_count_duplicates:
        distances = sorted(ds.distance.unique())[:number_of_vectors]
        return ds.loc[ds.distance <= max(distances)].drop('distance', axis=1)
    return ds.sort_values('distance', ascending=True).head(number_of_vectors).drop('distance', axis=1)

def predict(vector, dataset, number_of_neighbors=1, y='Survived'):
    neighbors = get_nearest_neighbor(vector, dataset, number_of_neighbors)
    return round(neighbors[y].mean())


def predict_testset(test_dataset, train_dataset, number_of_neighbors=1):
    ds = test_dataset.copy()
    select = selected + ['Survived']
    
    def predict_row(vector, dataset):
        if vector.name % 100 == 0:
            print(vector.name)
        return int(predict(vector, dataset[select], number_of_neighbors))

    ds['Survived'] = ds.loc[:, ds.columns.isin(selected)].apply(
        lambda x: predict_row(x, train_dataset), axis=1)
    
    return ds

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run()