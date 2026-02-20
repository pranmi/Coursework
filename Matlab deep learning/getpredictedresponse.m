function [predictedresponses,hidmx] = getpredictedresponse(thetavector,constants,thedata)
% USAGE: [predictedresponses,hidmx] = getpredictedresponse(thetavector,constants,thedata)

% Get Predicted Responses using "getpredictedresponse.m"
% The ith column of "hidmx" is the activation pattern over the
% H hidden units for the ith input pattern which is the
% ith row of "inputvectors" (see definition of "inputvectors" below)
%
% The ith column of the row vector "predictedresponses" is the activity
% of the ith output unit given the ith input pattern which is the ith
% row of input vectors (see definition of "inputvectors" below)


% Unpack Constants
nrhidden = constants.nrhidden;

% Unpack Event History (same as "gradobjfunction.m")
eventhistory = thedata.eventhistory;
nrtargets = thedata.nrtargets;
[nrstim,nrvars] = size(eventhistory);

% Get "desiredresponses". The ith element of column vector "desired response" 
% is the desired response
% for the ith row of the matrix "inputvectors". The matrices "desiredresponse"
% and "inputvectors" comprise the "training data set"
% 
% The column vector "desiredresponse" has length equal to the number of training vectors "nrstim"
% The matrix "inputvectors" is defined such that the desired response to the "jth" row of
% "inputvectors" is the "jth" element of the column vector of "desiredresponse"
% The dimension of an inputvector is referred to as "inputvectordim" in the code and "D" in the comments
desiredresponse = eventhistory(:,(1:nrtargets));
inputvectors = eventhistory(:,(nrtargets+1):nrvars);
[nrstim,inputvectordim] = size(inputvectors);

% Unpack parameter values
% Let H be number of hidden units. Let each input vector have
% dimension D. 
% wmatrix: matrix with H rows and D columns as defined in problem
% vmatrix: matrix with 1 rows and H+1 columns as defined in problem
[wmatrix,vmatrix] = unpackparameters(thetavector,constants,thedata);

% Now Compute Responses to Hidden Units 
% You will create a matrix called "hidmx" which has H rows and "nrstim" columns
% whose ith column is a "recoding" of the ith input vector which is the "ith" row of "inputvectors"
for i = 1:nrstim
    s_i = inputvectors(i,:)';            % column vector (D x 1)
    net_h = wmatrix * s_i;               % (H x 1)
    hidmx(:,i) = logisticsigmoid(net_h); % apply σ elementwise
end



% Now compute output unit responses (i.e., predicted responses) as a row vector whose ith element
% is the response to the ith input vector
predictedresponses = zeros(1,nrstim); % student compute this in several lines of code
for i = 1:nrstim
    h_i = hidmx(:,i);         % H x 1
    h_i_aug = [h_i; 1];       % (H+1) x 1
    net_output = vmatrix * h_i_aug;   % scalar (1x(H+1) times (H+1)x1)
    predictedresponses(i) = logisticsigmoid(net_output);
end