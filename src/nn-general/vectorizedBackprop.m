function [A, D] = vectorizedBackprop(A, Y, thetas, afun, dafun, verbose)	
m = size(A, 1);
A = A';

numThetas = size(thetas, 2);
numLayers = numThetas + 1;

Acells = {A};
Zcells = {};
Dcells = {};

for i = 1:numThetas
	[A, Z] = activate(A, thetas{i}, afun);
	
	if (i == numThetas)
		% remove bias from output layer
		A = A(2:end, :);
	end
	
	Acells{i + 1} = A;
	Zcells{i + 1} = Z;
end

% L(i) by m (output layer is L(i) by m)
Dcells{numLayers} = A - Y';

for i = numThetas:-1:1
	% use 'A' from layer i, d from layer i + 1
	D{i} = Dcells{i + 1} * Acells{i}';
	
	if (i != 1)
		Dcells{i} = (thetas{i}(:,2:end)' * Dcells{i + 1}) .* dafun(Zcells{i});
	end
end

end
