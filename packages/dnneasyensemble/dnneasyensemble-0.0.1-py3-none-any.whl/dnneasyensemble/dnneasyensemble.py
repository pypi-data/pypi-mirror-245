import os
from imblearn.combine import SMOTETomek
from imblearn.over_sampling import SMOTE, BorderlineSMOTE, ADASYN, SMOTENC
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
import tensorflow as tf
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, \
    roc_auc_score,  average_precision_score

def create_balanced_subsets(x, y, balance_flag=False, balance_strategy=None, sampling_strategy=0.2
                            , categorical_features=None, num_set='auto'):
    """

    :param x: 训练集x
    :param y: 训练集x对应y
    :param balance_flag: 是否运用数据采样处理方法
    :param balance_strategy: 采用哪样数据不平衡方法，默认smote
    :param sampling_strategy: 采样样本比例，默认0.2
    :param categorical_features: 如果是smotenc，传入分类特征序列列表
    :param num_set: 训练多少个模型，默认数据不平衡比例
    :return:
    """
    # Separate minority and majority class indices
    minority_indices = np.where(y == 1)[0]
    majority_indices = np.where(y == 0)[0]
    num_subsets = len(majority_indices) // len(minority_indices)
    print("----------目前多数类是少数类的{:d}倍-----------".format(num_subsets))
    # Calculate the number of minority samples in each subset
    if balance_flag:
        print("----------开始进行数据不平衡采样------------")
        if balance_strategy is None or balance_strategy == 'smotetomek':
            sample_way = SMOTE(sampling_strategy=sampling_strategy, random_state=7)
        elif balance_strategy == 'smotetomek':
            sample_way = SMOTETomek(random_state=7, sampling_strategy=sampling_strategy)
        elif balance_strategy == 'boderline':
            sample_way = BorderlineSMOTE(random_state=7, kind="borderline-1",sampling_strategy=sampling_strategy)
        elif balance_strategy == 'adasyn':
            sample_way = ADASYN(random_state=42, sampling_strategy=sampling_strategy)
        elif balance_strategy == 'smotenc':
            sample_way = SMOTENC(sampling_strategy=sampling_strategy,
                           categorical_features=categorical_features,
                           random_state=0)
        x, y = sample_way.fit_resample(x, y)
        minority_indices = np.where(y == 1)[0]
        majority_indices = np.where(y == 0)[0]
        num_subsets = len(majority_indices) // len(minority_indices)
        print("-------------采样后多数类是少数类的{:d}倍------------".format(num_subsets))
    if num_set == 'auto':
        pass
    else:
        num_subsets = num_set
    subsets = []

    for _ in range(num_subsets):
        # Sample minority samples
        sampled_minority_indices = np.random.choice(majority_indices, len(minority_indices), replace=False)
        majority_indices = np.setdiff1d(majority_indices, sampled_minority_indices)
        # Combine minority and majority samples
        subset_indices = np.concatenate([sampled_minority_indices, minority_indices])
        np.random.shuffle(subset_indices)
        # Create the subset
        x_subset, y_subset = x.iloc[subset_indices, :], y.iloc[subset_indices]
        subsets.append((x_subset, y_subset))
    return subsets

def train_dnn_model_easyensemble(subsets,basemodel,save_path,training_params=None):
    """
    无验证集，无早停通用版本
    :param subsets:数据集
    :param basemodel:dnn基模型
    :param save_path:保存路径
    :param training_params:训练参数
    :return:
    """
    save_path = save_path
    if training_params is None:
        training_params = {
                        'metrics': [tf.keras.metrics.Recall(), tf.keras.metrics.Precision()],
                        'optimizer': tf.keras.optimizers.Adam(learning_rate=1e-5),
                        'loss': 'binary_crossentropy',
                        'batch_size': 64,
                        'epochs': 300
                        }
    # 循环训练并保存模型
    for i, (x_subset, y_subset) in enumerate(subsets):
        # 创建并训练模型
        print(f'---------------第 {i + 1} 个模型开始训练------------------')
        model = basemodel
        metrics = training_params['metrics']
        model.compile(optimizer=training_params['optimizer'], loss=training_params['loss'],
                      metrics=metrics)

        history = model.fit(
            x=x_subset,
            y=y_subset,
            batch_size=training_params['batch_size'],
            epochs=training_params['epochs'],
            verbose=2
        ).history
        # 保存模型
        model_filename = os.path.join(save_path, f'model_subset_{i + 1}.h5')
        model.save(model_filename)
        print(f'---------------第 {i + 1} 个模型被存在 {model_filename}------------------')



def train_dnn_model_easyensemble_val(subsets,basemodel,save_path,training_params=None):
    """
    有验证集有早停通用版
    :param subsets:数据集
    :param basemodel:dnn基模型
    :param save_path:保存路径
    :param training_params:训练参数
    :return:
    """
    save_path = save_path
    # 循环训练并保存模型
    if training_params is None:
        training_params = {
                        'metrics': [tf.keras.metrics.Recall(), tf.keras.metrics.Precision()],
                        'optimizer': tf.keras.optimizers.Adam(learning_rate=1e-5),
                        'loss': 'binary_crossentropy',
                        'callbacks': [ReduceLROnPlateau(monitor='val_loss', min_lr=1e-6),EarlyStopping(monitor='val_loss', patience=10)],
                        'batch_size': 64,
                        'epochs': 500
                        }
    for i, (x_subset, y_subset) in enumerate(subsets):
        # 创建并训练模型
        print(f'---------------第 {i + 1} 个模型开始训练------------------')
        model = basemodel
        x_train_subset, x_test_subset, y_train_subset, y_test_subset = train_test_split(x_subset, y_subset, test_size=0.2,
                                                                            random_state=42)
        metrics = training_params['metrics']
        model.compile(optimizer=training_params['optimizer'], loss=training_params['loss'],
                      metrics=metrics)

        callbacks =training_params['callbacks']

        history = model.fit(
            x=x_train_subset,
            y=y_train_subset,
            batch_size=training_params['batch_size'],
            epochs=training_params['epochs'],
            verbose=2,
            callbacks=callbacks,
            validation_data=(x_test_subset, y_test_subset)
        ).history
        # 保存模型
        model_filename = os.path.join(save_path, f'model_subset_{i + 1}.h5')
        model.save(model_filename)
        print(f'---------------第 {i + 1} 个模型被存在 {model_filename}------------------')

def load_model_result(save_model_filename,x_test,y_test,voting_type='soft'):
    # 文件夹路径，存放模型文件
    model_folder = save_model_filename

    # 用于保存每个模型的预测结果
    all_predictions = []
    all_predictions_proba = []

# 遍历文件夹，加载模型并预测
    for file in os.listdir(model_folder):
        if file.endswith(".h5"):
            model_path = os.path.join(model_folder, file)
            model = tf.keras.models.load_model(model_path)  # 加载模型
            # 对测试集进行预测
            y_pred_proba = model.predict(x_test, batch_size=128)
            y_pred = (y_pred_proba > 0.5).astype(int)
            # 保存每个模型的预测结果
            all_predictions.append(y_pred)
            all_predictions_proba.append(y_pred_proba)

    # 输出指标
    if voting_type == 'soft':
        ensemble_predictions = np.mean(all_predictions_proba, axis=0)
        final_predictions = (ensemble_predictions > 0.5).astype(int)
    elif voting_type == 'hard':
        ensemble_predictions = np.mean(all_predictions, axis=0)
        final_predictions = (ensemble_predictions > 0.5).astype(int)
    else:
        raise ValueError("Invalid voting_type. Use 'soft' or 'hard'.")

    # 计算指标
    accuracy = accuracy_score(y_test, final_predictions)
    precision = precision_score(y_test, final_predictions)
    recall = recall_score(y_test, final_predictions)

    auc = roc_auc_score(y_test, ensemble_predictions)
    aucpr = average_precision_score(y_test, ensemble_predictions)

    print(f"Ensemble Accuracy: {accuracy}")
    print(f"Ensemble Precision: {precision}")
    print(f"Ensemble Recall: {recall}")
    print(f"Ensemble PR AUC: {aucpr}")
    print(f"Ensemble ROC AUC: {auc}")

def dnn_easyensemble(x_train,x_test,y_train,y_test,save_path,basemodel,load_filename,balanece_flag=False,balance_strategy=None
                     ,categorical_features=None,training_params=None,num_set='auto',sampling_strategy=0.2,voting_type='soft',val=True):
    if not os.path.exists(save_path):
        # 如果不存在，创建文件夹
        os.makedirs(save_path)
    subsets = create_balanced_subsets(x_train, y_train, balance_flag=balanece_flag, balance_strategy=balance_strategy
                                      , categorical_features=categorical_features, num_set=num_set, sampling_strategy=sampling_strategy)

    if val is True:
        train_dnn_model_easyensemble_val(subsets, basemodel, save_path, training_params=training_params)
    elif val is not True:
        train_dnn_model_easyensemble(subsets, basemodel, save_path, training_params=training_params)
    load_model_result(load_filename, x_test, y_test, voting_type)

