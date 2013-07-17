function W = debugInitializeWeights(networkStructure)

W = [];
epsilon_init = 0.12; 

numThetas = size(networkStructure, 2) - 1;
for i = 1:numThetas
	out = networkStructure(i + 1);
	in = networkStructure(i) + 1;	
	numel = out * in;
	
	% init W to sin values so that they are the same each time, to help with debugging
	W = [W; (sin(1:numel) / 10)'];
end

end
