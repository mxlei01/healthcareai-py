import numpy as np

import healthcareai.pipelines.data_preparation as hcai_pipelines
import healthcareai.trained_models.trained_supervised_model as hcai_tsm
from healthcareai.advanced_supvervised_model_trainer import AdvancedSupervisedModelTrainer
from healthcareai.common.healthcareai_error import HealthcareAIError


class SupervisedModelTrainer(object):
    """
    This class helps create a model using several common classifiers and regressors, both of which report appropiate
    metrics.
    """

    def __init__(self, dataframe, predicted_column, model_type, impute=True, grain_column=None, verbose=False):
        """
        Set up a SupervisedModelTrainer
        
        Args:
            dataframe (pandas.core.frame.DataFrame): The training data in a pandas dataframe
            predicted_column (str): The name of the prediction column 
            model_type (str): the trainer type - 'classification' or 'regression'
            impute (bool): True to impute data (mean of numeric columns and mode of categorical ones). False to drop rows
                that contain any null values.
            grain_column (str): The name of the grain column
            verbose (bool): Set to true for verbose output. Defaults to False.
        """
        self.predicted_column = predicted_column
        self.grain_column = grain_column

        # Validate the type of model, dataframe, and the predicted column before feeding the data to the pipeline
        self.model_input_validate(dataframe, model_type, predicted_column)

        # Build the pipeline
        # TODO This pipeline may drop nulls in prediction rows if impute=False
        # TODO See https://github.com/HealthCatalyst/healthcareai-py/issues/276
        pipeline = hcai_pipelines.full_pipeline(model_type, predicted_column, grain_column, impute=impute)

        # Run the raw data through the data preparation pipeline
        clean_dataframe = pipeline.fit_transform(dataframe)

        # Instantiate the advanced class
        self._advanced_trainer = AdvancedSupervisedModelTrainer(clean_dataframe, model_type, predicted_column,
                                                                grain_column, verbose)

        # Save the pipeline to the parent class
        self._advanced_trainer.pipeline = pipeline

        # Split the data into train and test
        self._advanced_trainer.train_test_split()

    @property
    def clean_dataframe(self):
        """ Returns the dataframe after the preparation pipeline (imputation and such) """
        return self._advanced_trainer.dataframe

    def model_input_validate(self, dataframe, model_type, predicted_column):
        """ Validate the dataset with the model_type and predicted_column.

        Args:
            dataframe (pandas.core.frame.DataFrame): The training data in a pandas dataframe
            model_type (str): the trainer type - 'classification' or 'regression'
            predicted_column (str): The name of the prediction column

        Returns:
            None

        """
        predicted_column_values = dataframe[predicted_column].dropna().unique()
        if model_type == "classification":
            # If the model type is classification, and if the predicted column is non binary, or the binary column
            # values are not 'N' and 'Y' then raise an error
            if len(predicted_column_values) > 2:
                raise HealthcareAIError("For model_type=classification, the prediction column should be binary, "
                                        "since it contains %s, which is more than 2 values" % predicted_column_values)
            elif len(predicted_column_values) == 1:
                raise HealthcareAIError("For model_type=classification, the prediction column should be binary, "
                                        "since it contains %s, which is equal to 1 value" % predicted_column_values)
            elif set(predicted_column_values) != {"Y", "N"}:
                raise HealthcareAIError("For model_type=classification, the prediction column should only hold N or Y, "
                                        "since it contains %s, which is not Y or N" % predicted_column_values)
        elif model_type == "regression":
            # If the model type is regression, and if the predicted column is binary, or if the data contains
            # non numeric data
            if len(predicted_column_values) <= 2:
                raise HealthcareAIError("For model_type=regression, the prediction column should not be binary, "
                                        "since it contains %s, which less or equal to 2 values" % predicted_column_values)
            if not dataframe[predicted_column].apply(np.isreal).unique()[0]:
                raise HealthcareAIError("For model_type=regression, all values in the prediction column should only be "
                                        "numerical data")

    def random_forest(self, save_plot=False):
        # TODO Convenience method. Probably not needed?
        """ Train a random forest model and print out the model performance metrics.

        Args:
            save_plot (bool): For the feature importance plot, True to save plot (will not display). False by default to
                display.

        Returns:
            TrainedSupervisedModel: A trained supervised model.
        """
        if self._advanced_trainer.model_type is 'classification':
            return self.random_forest_classification(save_plot=save_plot)
        elif self._advanced_trainer.model_type is 'regression':
            return self.random_forest_regression()

    def knn(self):
        """ Train a knn model and print out the model performance metrics.
        
        Returns:
            TrainedSupervisedModel: A trained supervised model.
        """
        model_name = 'KNN'
        print('\nTraining {}'.format(model_name))

        # Train the model
        trained_model = self._advanced_trainer.knn(scoring_metric='roc_auc', hyperparameter_grid=None,
                                                   randomized_search=True)

        # Display the model metrics
        trained_model.print_training_results()

        return trained_model

    def random_forest_regression(self):
        """ Train a random forest regression model and print out the model performance metrics.

        Returns:
            TrainedSupervisedModel: A trained supervised model.
        """
        model_name = 'Random Forest Regression'
        print('\nTraining {}'.format(model_name))

        # Train the model
        trained_model = self._advanced_trainer.random_forest_regressor(trees=200,
                                                                       scoring_metric='neg_mean_squared_error',
                                                                       randomized_search=True)

        # Display the model metrics
        trained_model.print_training_results()

        return trained_model

    def random_forest_classification(self, save_plot=False):
        """ Train a random forest classification model, print out performance metrics and show a feature importance plot.
        
        Args:
            save_plot (bool): For the feature importance plot, True to save plot (will not display). False by default to
                display.

        Returns:
            TrainedSupervisedModel: A trained supervised model.
        """

        model_name = 'Random Forest Classification'
        print('\nTraining {}'.format(model_name))

        # Train the model
        trained_model = self._advanced_trainer.random_forest_classifier(trees=200, scoring_metric='roc_auc',
                                                                        randomized_search=True)

        # Display the model metrics
        trained_model.print_training_results()

        # Save or show the feature importance graph
        hcai_tsm.plot_rf_features_from_tsm(trained_model, self._advanced_trainer.x_train, save=save_plot)

        return trained_model

    def logistic_regression(self):
        """ Train a logistic regression model and print out the model performance metrics.
        
        Returns:
            TrainedSupervisedModel: A trained supervised model.
        """
        model_name = 'Logistic Regression'
        print('\nTraining {}'.format(model_name))

        # Train the model
        trained_model = self._advanced_trainer.logistic_regression(randomized_search=False)

        # Display the model metrics
        trained_model.print_training_results()

        return trained_model

    def linear_regression(self):
        """ Train a linear regression model and print out the model performance metrics.
        
        Returns:
            TrainedSupervisedModel: A trained supervised model.
        """
        model_name = 'Linear Regression'
        print('\nTraining {}'.format(model_name))

        # Train the model
        trained_model = self._advanced_trainer.linear_regression(randomized_search=False)

        # Display the model metrics
        trained_model.print_training_results()

        return trained_model

    def ensemble(self):
        """ Train a ensemble model and print out the model performance metrics.
        
        Returns:
            TrainedSupervisedModel: A trained supervised model.
        """
        # TODO consider making a scoring parameter (which will necessitate some more logic
        model_name = 'ensemble {}'.format(self._advanced_trainer.model_type)
        print('\nTraining {}'.format(model_name))

        # Train the appropriate ensemble of models
        if self._advanced_trainer.model_type is 'classification':
            metric = 'roc_auc'
            trained_model = self._advanced_trainer.ensemble_classification(scoring_metric=metric)
        elif self._advanced_trainer.model_type is 'regression':
            # TODO stub
            metric = 'neg_mean_squared_error'
            trained_model = self._advanced_trainer.ensemble_regression(scoring_metric=metric)

        print(
            'Based on the scoring metric {}, the best algorithm found is: {}'.format(metric,
                                                                                     trained_model.algorithm_name))

        # Display the model metrics
        trained_model.print_training_results()

        return trained_model

    @property
    def advanced_features(self):
        """ Returns the underlying AdvancedSupervisedModelTrainer instance. For advanced users only. """
        return self._advanced_trainer
