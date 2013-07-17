% a - a single training example, bias included
% y - actual classification of training example as bit vector (y = 3 as [0, 0, 1])
% thetas - the neural network parameters as a cell array of the matrices for each layer
% afun - the node activation function
% dafun - the derivative of the node activation function
% verbose - whether to print out each computed layer of the network

% return a - the output of the neural network
% return D - cell array of the matrices of the partial derivatives with respect to each parameter
function [a, D] = backprop(a, y, thetas, afun, dafun, verbose)	
	% gradient matrices
	grad_deltas = {};
	% initialize a nodes with training example
	aNodes = {a};
	% no z nodes for training example
	zNodes = {};	
	
	% forward propagation
	numThetas = size(thetas, 2);
	for i = 1:numThetas		
		% calculate input nodes for next layer
		[a, z] = activate(a, thetas{i}, afun);		
		
		% show layer nodes in verbose mode
		if (verbose)
			fprintf("Layer %d:\n\n", i + 1);
			a
		end	
		
		% save computed nodes (as columns instead of rows, for easier computation later) 
		% to use in backpropagation
		aNodes{i+1} = a;
		zNodes{i+1} = z;
	end
	
	% remove bias unit on output layer
	a = a(2:end);
	
	% backpropagation
	
	% compute d(L)
	d = a - y';
	
	% start with output layer
	for i = numThetas:-1:1
		% use 'a' from layer i, d from layer i + 1
		D{i} = d * aNodes{i}';		
		
		% d does not apply to the input data
		if (i != 1) 
			% d does not apply to the bias unit
			d = (thetas{i}(:,2:end)' * d) .* dafun(zNodes{i});
		end
	end
end