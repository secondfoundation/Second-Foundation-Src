function [J unrolledThetaGrad] = nnCostFunctionGeneral(nnParams, networkStructure, X, y, lambda, afun, dxafun)

% Implements the neural network cost function for an arbitrary
% neural network which performs classification.
%
% Computes the cost and gradient of the neural network. The
% parameters for the neural network are "unrolled" into the vector
% nn_params and need to be converted back into the weight matrices. 
% 
% The returned parameter grad should be a "unrolled" vector of the
% partial derivatives of the neural network.

m = size(X, 1);
X = [ones(m, 1), X];       

numLabels = networkStructure(end);
thetas = shapeNNParams(nnParams, networkStructure);
numThetas = size(thetas, 2);

thetaGrads = {};
for i = 1:numThetas
	thetaGrads{i} = zeros(size(thetas{i}));
end

% Change y values to bit vectors
yBit = zeros(m,numLabels);
for i = 1:m
  bits = zeros(1,numLabels);
  bits(y(i)) = 1;
  yBit(i,:) = bits;
end

	fprintf("another cost");

% compute cost and gradients
J = 0;
for i = 1:m
	x = X(i,:)';	
	y = yBit(i,:);
	
	[h, partialGrad] = backprop(x, y, thetas, afun, dxafun, false);
	
	J += -y * log(h) - (1 - y) * log(1 - h); 	
	
	for i = 1:numThetas
		thetaGrads{i} += partialGrad{i};
	end
end

J *= (1 / m);

regSum = 0;
for i = 1:numThetas
	% don't regularize bias column
	regSum += sum(sum(thetas{i}(:,2:end) .^ 2));
end

J += (lambda / (2*m)) * regSum;

unrolledThetaGrad = [];

for i = 1:numThetas
    tgrad = thetaGrads{i};
 	tgrad *= (1/m);
	
	% don't regularize bias params
    tgrad(:,2:end) += (lambda / m) * thetas{i}(:,2:end);
	
 	unrolledThetaGrad = [unrolledThetaGrad; tgrad(:)];
end
