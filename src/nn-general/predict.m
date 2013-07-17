function [val, p] = predict(X, nnParams, networkStructure, afun)

m = size(X, 1);
A = [ones(m, 1) X]';

thetas = shapeNNParams(nnParams, networkStructure);
numThetas = size(thetas, 2);

for i = 1:numThetas
	[A, Z] = activate(A, thetas{i}, afun);
end

% remove bias from output layer
A = A(2:end, :)';

[val, p] = max(A,[],2);

end
