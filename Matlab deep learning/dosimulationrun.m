% Initial Setup

% SET LAMBDA
% Change the regularization constant lambda
lambda = input('What is the regularization constant LAMBDA? (0 or 0.02)?');
runid = input('Which simulation run is this (e.g., 1,2, or 3):?')
fileprefixname = ['lambda',num2str(lambda*100),'run',num2str(runid)];
diary([fileprefixname,'.txt']);
%lambda = 0.0;

%-----------------------------
% SET OTHER CONSTANTS
learningrate = 1;
constants.learningrate = learningrate;
constants.maxiterations = 60000;
constants.maxgradINFnorm = 0.0003;
constants.momentumconstant = 0.1;
constants.displayfreq = 1000;
constants.lambda = lambda;
constants.nrhidden = 30;
constants

% Load Data Set
datasetfilename = 'recodedcar.xlsx';
entiredatafile = xlsread(datasetfilename);
[nrstim,nrvars] = size(entiredatafile);
randindex = randperm(nrstim);
permuteddatafile = entiredatafile(randindex,:);

% Create and save two halves of the permuted data set
halfIndex = round(nrstim / 2);
rawDataSet1 = permuteddatafile(1:halfIndex, :);
rawDataSet2 = permuteddatafile(halfIndex+1:end, :);
xlswrite('DataSet1.xlsx',rawDataSet1)
xlswrite('DataSet2.xlsx',rawDataSet2)

% Learn Data Set 1 and Test on Data Set 2
tstart = tic; % Start Timer
disp(['STARTING SIMULATION RUN WITH LAMBDA = ',num2str(constants.lambda)]);
disp('--------Training on Data Set 1----------------')
nrtargets = 1;
thedata1 = makethedataset('DataSet1.xlsx',nrtargets);
[nrevents,nrvars] =size(thedata1.eventhistory);
inputvectordim = nrvars - nrtargets;
thetavectordim = (constants.nrhidden + 1) + (constants.nrhidden*inputvectordim);
thetavector = randn(thetavectordim,1);
[finalthetavector1, trainTotalError1, trainIterations1, trainGradMax1] = ...
    gobatchgradientdescent(thetavector, constants,thedata1);
disp('---------Using Parameters from Training on Data Set 1 to do Testing on Data Set 2--------------');
thedata2 = makethedataset('DataSet2.xlsx',nrtargets);
constants.learningrate = 0;
[testFinalThetaVector2, testTotalError2, testIterations2, testGradMax2] = ...
    gobatchgradientdescent(finalthetavector1, constants, thedata2);
disp('---------- Training on Data Set 2--------------------')
% Learn Data Set 2 and Test on Data Set 1
constants.learningrate = learningrate;
[finalthetavector3, trainTotalError2, trainIterations2, trainGradMax2] = ...
    gobatchgradientdescent(thetavector, constants,thedata2);
disp('---------Using Parameters from Training on Data Set 2 to do Testing on Data Set 1--------------');
% Test the learned parameters on Data Set 1
constants.learningrate = 0;
[testFinalThetaVector1, testTotalError1, testIterations1, testGradMax1] = ...
    gobatchgradientdescent(finalthetavector3, constants, thedata1);
totaltime = toc(tstart); % stop timer

disp(['=========================================================='])
disp('**************** FINAL RESULTS ******************');
[trainempiricalrisk1,trainHidRegTerm1,trainhidmx1] = objfunction(finalthetavector1,constants,thedata1);
[trainempiricalrisk2,trainHidRegTerm2,trainhidmx2] = objfunction(finalthetavector3,constants,thedata2);
[testempiricalrisk1,testHidRegTerm1,testhidmx1] = objfunction(finalthetavector1,constants,thedata2);
[testempiricalrisk2,testHidRegTerm2,testhidmx2] = objfunction(finalthetavector3,constants,thedata1);
trainpredictError1 = trainempiricalrisk1 - (lambda/2)*trainHidRegTerm1;
trainpredictError2 = trainempiricalrisk2 - (lambda/2)*trainHidRegTerm2;
testpredictError1 = testempiricalrisk1 - (lambda/2)*testHidRegTerm1;
testpredictError2 = testempiricalrisk2 - (lambda/2)*testHidRegTerm2;
disp(['Training PREDICTION Error Data Set 1:',num2str(trainpredictError1),', Test PREDICTION Error Data Set 1:',num2str(testpredictError1)]);
disp(['Training PREDICTION Error Data Set 2:',num2str(trainpredictError2),', Test PREDICTION Error Data Set 2:',num2str(testpredictError2)]);
avgtrainpredict = (trainpredictError1+trainpredictError2)/2;
avgtestpredict = (testpredictError1 + testpredictError2)/2;
disp(['Average TRAINING prediction error: ',num2str(avgtrainpredict),', Average TESTING prediction error:',num2str(avgtestpredict)]);
disp(['Elapsed Time = ',num2str(totaltime),' seconds.']);


% "hiddenactivity" is a row vector whose dimension is equal to the number of
% hidden units. The Kth element of "hiddenactivity" is the standard deviation of the kth
% hidden unit across the training data.
trainhiddenactivity1 = std(trainhidmx1');
testhiddenactivity1 = std(testhidmx1');
trainhiddenactivity2 = std(trainhidmx2');
testhiddenactivity2 = std(testhidmx2');

subplot(221);
bar(trainhiddenactivity1)
ylabel('Std. Dev. Activity Level');
xlabel('Hidden Unit ID');
title(['Hidden Unit Variance (Training Data Set 1), lambda = ',num2str(lambda)]);;

subplot(222);
bar(trainhiddenactivity2)
ylabel('Std. Dev. Activity Level');
xlabel('Hidden Unit ID');
title(['Hidden Unit Variance (Training Data Set 2), lambda = ',num2str(lambda)]);

subplot(223);
bar(testhiddenactivity1)
ylabel('Std. Dev. Activity Level');
xlabel('Hidden Unit ID');
title(['Hidden Unit Variance (Testing Data Set 1), lambda = ',num2str(lambda)]);

subplot(224);
bar(testhiddenactivity2)
ylabel('Std. Dev. Activity Level');
xlabel('Hidden Unit ID');
title(['Hidden Unit Variance (Testing Data Set 2), lambda = ',num2str(lambda)]);
savefig([fileprefixname,'.fig'])
diary('off');