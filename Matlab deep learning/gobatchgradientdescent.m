function [finalthetavector,totalerror, nriterations, finalgradmax] = ...
    gobatchgradientdescent(thetavector, constants,thedata)

    keepgoing = 1;
    iteration = 0;
    learningrate = constants.learningrate;
    maxiterations = constants.maxiterations;
    maxgradINFnorm = constants.maxgradINFnorm;
    momentumconstant = constants.momentumconstant;
    displayfreq = constants.displayfreq;
    
    lastsearchdirection = zeros(size(thetavector));  % Initialize last search direction
    lastthetavector = zeros(size(thetavector));
    while keepgoing,
         %evaluate gradient of error function
         gradientvector = gradobjfunction(thetavector, constants, thedata);
         % Update Parameter values
         searchdirection = -gradientvector + momentumconstant * lastsearchdirection;
         thetavector = thetavector + learningrate * searchdirection;
         lastsearchdirection = searchdirection;
         
         % Update iteration counter
         iteration = iteration + 1
         
         % compute Infinity norm of the gradient vector
         gradINFnorm = max(abs(gradientvector));
         
         % Set "keepgoing = 0" if iterations exceed "maxiterations" or if Infinity norm of gradient is
         % less than or equal to "maxgradINFnorm" otherwise set "keepgoing
         % = 1" or there is no change in the parameter vector value
         toomanyiterations = (iteration > maxiterations);
         gradinfnorm2small = (gradINFnorm <= maxgradINFnorm);
         noparameterchange = max(abs(thetavector - lastthetavector)) < eps;
         learningrateiszero = (learningrate == 0);
         keepgoing = ~toomanyiterations & ~gradinfnorm2small & ~noparameterchange & ~learningrateiszero;
         lastthetavector = thetavector;
        
         % display status
         if ((round(iteration/displayfreq) == (iteration/displayfreq)) | ~keepgoing),
            [totalerror,HidRegTerm,hiddenactivity] = objfunction(thetavector,constants,thedata);
            disp(['Iteration #',num2str(iteration), ': Error = ', num2str(totalerror),...
                    ', gradnorm = ',num2str(gradINFnorm),', Hidden Unit Activity = ',num2str(HidRegTerm)])
         end; % end if statement
    
    end  % end while loop
    finalgradmax = gradINFnorm;
    nriterations = iteration;
    finalthetavector = thetavector;
end   % end main program