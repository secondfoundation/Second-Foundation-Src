% x - one or more training examples as column vectors (n by m, where n is the number of features, m the number of examples)
% theta - parameters matrix to produce next network layer from the input layer x
% afun - the activation function to apply to each node

% return a - the next network layer, after applying the activation function
% return z - the next network layer, before applying the activation function
function [a, z] = activate(x, theta, afun)
	z = theta * x;
	a = afun(z);
	
	% add bias to a
	m = size(x, 2);
	a = [ones(1, m); a];
end