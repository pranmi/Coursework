function [empiricalrisk,HidRegTerm,hidmx] = objfunction(thetavector,constants,thedata)
% USAGE: [empiricalrisk,HidRegTerm,hidmx] = objfunction(thetavector,constants,thedata)

% "empiricalrisk" is a scalar which corresponds to the definition "empirical risk objective function" in problem.
% It is the empirical risk function whose loss function includes both the prediction error and hidden unit minimization term.

% "HidRegTerm" (scalar) is the average magnitude of the hidden unit activations (compute sum of the squares of the hidden unit
% activations for a particular data record...then average across data records) 

% "hidmx" is computed from "getpredictedresponse" (matrix)

% Unpack Event History 
eventhistory = thedata.eventhistory;
nrtargets = thedata.nrtargets;
[nrstim,nrvars] = size(eventhistory);
desiredresponse = thedata.eventhistory(:,1);

% Now Compute Responses to Hidden Units 
% Get Predicted Responses using "getpredictedresponses.m"
% The ith column of "hidmx" is the activation pattern over the
% H hidden units for the ith input pattern which is the
% ith row of "inputvectors"
%
% The ith column of the row vector "predictedresponses" is the activity
% of the ith output unit given the ith input pattern which is the ith
% row of input vectors
[predictedresponses,hidmx] = getpredictedresponse(thetavector,constants,thedata);

% Compute the prediction error Function 
lambda = constants.lambda;

predicterrors = zeros(1,nrstim);
for i = 1:nrstim
    y    = desiredresponse(i);
    yhat = predictedresponses(i);
    predicterrors(i) = -( y*log(yhat) + (1-y)*log(1-yhat) );
end
PredictionErrorTerm = (1/nrstim) * sum(predicterrors);
% COMPUTE Regularization Term "HidRegTerm" which is the "average hidden unit magnitude" as defined above.
HidRegTerm = sum(sum(hidmx.^2)) / nrstim;

% Compute empirical risk
empiricalrisk = PredictionErrorTerm + (lambda/2)*HidRegTerm;


end % end of main function