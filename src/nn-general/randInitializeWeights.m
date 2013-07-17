% Randomly initializes parameters for each layer of a neural network.

% layerStructure - a row vector containing the number of nodes in each layer, including the input and output layers
% return W - a cell array of the randomly inidialized weight matrices for each layer
function W = randInitializeWeights(networkStructure)

W = [];
epsilon_init = 0.12; 

numThetas = size(networkStructure, 2) - 1;
for i = 1:numThetas
	out = networkStructure(i + 1);
	in = networkStructure(i) + 1;	
	numel = out * in;
	
	% init W to sin values so that they are the same each time, to help with debugging
	W = [W; rand(numel, 1) * 2 * epsilon_init - epsilon_init];
end

end
