%% Machine Learning Online Class - Exercise 4 Neural Network Learning

%  Instructions
%  ------------
% 
%  This file contains code that helps you get started on the
%  linear exercise. You will need to complete the following functions 
%  in this exericse:
%
%     sigmoidGradient.m
%     randInitializeWeights.m
%     nnCostFunction.m
%
%  For this exercise, you will not need to change any code in this file,
%  or any other files other than those mentioned above.
%

%% Initialization
clear ; close all; clc

%% Setup the parameters you will use for this exercise
input_layer_size  = 400;  % 20x20 Input Images of Digits
num_labels = 10;          % 10 labels, from 1 to 10   
                          % (note that we have mapped "0" to label 10)

networkStructure = [input_layer_size, 25, 25, num_labels];
lambda = 0;

afun = @sigmoid;
dxafun = @sigmoidGradient;

%% =========== Part 1: Loading and Visualizing Data =============
%  We start the exercise by first loading and visualizing the dataset. 
%  You will be working with a dataset that contains handwritten digits.
%

% Load Training Data
fprintf('Loading and Visualizing Data ...\n')

load('ex4data1.mat');
m = size(X, 1);

pctTrain = 0.6;
pctCV = 0.2;
pctTest = 0.2;

dataSize = size(X, 1);

trainEnd = floor(dataSize * pctTrain);
cvEnd = floor(dataSize * (pctTrain + pctCV));

rowSample = randperm(dataSize);

Xtrain = X(rowSample(1:trainEnd), :);
Xcv = X(rowSample(trainEnd + 1:cvEnd), :);
Xtest = X(rowSample(cvEnd + 1:end), :);

Ytrain = y(rowSample(1:trainEnd), :);
Ycv = y(rowSample(trainEnd + 1:cvEnd), :);
Ytest = y(rowSample(cvEnd + 1:end), :);

% Randomly select 100 data points to display
sel = randperm(size(X, 1));
sel = sel(1:100);

displayData(X(sel, :));

fprintf('Program paused. Press enter to continue.\n');
pause;

initial_nn_params = randInitializeWeights(networkStructure);

%% =================== Part 8: Training NN ===================
%  You have now implemented all the code necessary to train a neural 
%  network. To train your neural network, we will now use "fmincg", which
%  is a function which works similarly to "fminunc". Recall that these
%  advanced optimizers are able to train our cost functions efficiently as
%  long as we provide them with the gradient computations.
%
fprintf('\nTraining Neural Network... \n')

%  After you have completed the assignment, change the MaxIter to a larger
%  value to see how more training helps.
options = optimset('MaxIter', 150);

% Create "short hand" for the cost function to be minimized
costFunction = @(p) nnCostFunctionVec(p, networkStructure, Xtrain, Ytrain, lambda, afun, dxafun);

% Now, costFunction is a function that takes in only one argument (the
% neural network parameters)
[nn_params, cost] = fmincg(costFunction, initial_nn_params, options);

fprintf('Program paused. Press enter to continue.\n');
pause;


%% ================= Part 9: Visualize Weights =================
%  You can now "visualize" what the neural network is learning by 
%  displaying the hidden units to see what features they are capturing in 
%  the data.

fprintf('\nVisualizing Neural Network... \n')

% TODO display general network in some way
% displayData(Theta1(:, 2:end));

fprintf('\nProgram paused. Press enter to continue.\n');
pause;

%% ================= Part 10: Implement Predict =================
%  After training the neural network, we would like to use it to predict
%  the labels. You will now implement the "predict" function to use the
%  neural network to predict the labels of the training set. This lets
%  you compute the training set accuracy.

[val, pred] = predict(Xtrain, nn_params, networkStructure, afun);

fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred == Ytrain)) * 100);

[val, pred] = predict(Xcv, nn_params, networkStructure, afun);

fprintf('\nCV Set Accuracy: %f\n', mean(double(pred == Ycv)) * 100);

[val, pred] = predict(Xtest, nn_params, networkStructure, afun);

fprintf('\nTest Set Accuracy: %f\n', mean(double(pred == Ytest)) * 100);


