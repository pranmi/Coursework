function thedata = makethedataset(thedatafilename,numberoftargets);
% USAGE: thedata = makethedataset(thedatafilename,numberoftargets);

% Setup Data Set Constants
% Note that first row of spreadsheet is the names of the variables
% Each additional row is a training stimulus
% The first M columns are the "targets" (desired responses)
thedata.datafilename = thedatafilename; 
[eventhistory, varnames, alldata] = xlsread(thedatafilename);
thedata.eventhistory = eventhistory;
thedata.varnames = varnames;
thedata.nrtargets = numberoftargets; 
[nrevents,nrvars] = size(eventhistory);
nrtargets = thedata.nrtargets;
thedata.nrvars = nrvars;
thedata.inputvectordim = (nrvars - nrtargets);
thedata.inputvectors = eventhistory(:,(nrtargets+1):nrvars);
thedata.targetvectors = eventhistory(:,(1:nrtargets));
thedata.nrrecords = nrevents;
disp(['Datafile: "',thedatafilename,'" loaded!',...
    ' Number predictors =',num2str(thedata.inputvectordim),', Number targets = ',num2str(nrtargets),...
    ', Number of records =', num2str(nrevents)]);
end

