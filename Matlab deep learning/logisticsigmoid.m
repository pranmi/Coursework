% DEFINE USEFUL FUNCTIONS HERE
    function y = logisticsigmoid(x)
        y = 1 ./ (1 + exp(-x));
    end