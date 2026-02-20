function gradientvector = gradobjfunction(thetavector,constants,thedata)
% USAGE: gradientvector = gradobjfunction(thetavector,constants,thedata)

% "gradientvector" is a column vector defined such that the first
% set of H+1 elements are defined as the derivative of the objective
% function with respect to the row vector "vmatrix" and whose second
% set of D elements are defined as the derivative of the objective
% function with respect to the connection weights from the input
% units to the first hidden unit and whose third set of elements
% are defined as the derivative of the objective function with respect
% to the second hidden unit and so on... (H is the number of hidden units
% and D is the number of input units)

% Unpack constants
lambda = constants.lambda;
nrhidden = constants.nrhidden;

% Unpack Event History 
eventhistory = thedata.eventhistory;
nrtargets = thedata.nrtargets;
[nrstim,nrvars] = size(eventhistory);
desiredresponse = thedata.eventhistory(:,1);
desiredresponseT = desiredresponse';
inputvectors = eventhistory(:,(nrtargets+1):nrvars);
[nrstim,inputvectordim] = size(inputvectors);

% Unpack parameter values
% Let H be number of hidden units. Let each input vector have
% dimension D. 
% wmatrix: matrix with H rows and D columns as defined in problem
% vmatrix: matrix with 1 rows and H+1 columns as defined in problem
[wmatrix,vmatrix] = unpackparameters(thetavector,constants,thedata);

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

% Compute derivative of Empirical Risk with respect to V vector
dcdv = zeros(nrstim,(nrhidden+1));
for i = 1:nrstim,
    % student fix this line of code and add more lines if necessary
    y_hat_i = predictedresponses(i);
    y_i = desiredresponse(i);
    h_i = hidmx(:,i);
    h_i_augmented = [h_i; 1];
    dcdv(i,:) = (y_hat_i - y_i) * h_i_augmented';
end;
dldv = mean(dcdv, 1)';
    % student fix this line of code and add more lines if necessary
% Compute derivative of Empirical Risk with respect to kth row of W matrix
dcdwisum = zeros(nrhidden,inputvectordim);
for i = 1:nrstim,
    dcdwi = zeros(nrhidden,inputvectordim);
    for k = 1:nrhidden,
       y_hat_i = predictedresponses(i);
       y_i = desiredresponse(i);
       s_i = inputvectors(i,:)';
       h_i = hidmx(:,i);
       h_ik = h_i(k);
       v_k = vmatrix(k);
       dEdw_k = (y_hat_i - y_i) * v_k * h_ik * (1 - h_ik) * s_i';
       dReg_dw_k = 2 * h_ik * h_ik * (1 - h_ik) * s_i';
       dcdwi(k,:) = dEdw_k + (lambda/2) * dReg_dw_k;
    end;
    dcdwisum = dcdwisum + dcdwi;
end;
dldw = dcdwisum/nrstim;
dldwT = dldw';

% Compute Final Gradient Vector

% STUDENT: Compute Derivative of Objective Function with
% with respect to the learning machine's parameters
% This is a vector called "gradientvector" whose first
% set of H+1 elements are defined as the derivative of the objective
% function with respect to the row vector "vmatrix" and whose second
% set of D elements are defined as the derivative of the objective
% function with respect to the connection weights from the input
% units to the first hidden unit and whose third set of elements
% are defined as the derivative of the objective function with respect
% to the second hidden unit and so on...
gradientvector = [dldv; dldwT(:)];
% student fix this line of code and add more lines if necessary
end