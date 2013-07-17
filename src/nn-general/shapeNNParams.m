function matrixCells = shapeNNParams(nnParamVector, networkStructure)

matrixCells = {};

numThetas = size(networkStructure, 2) - 1;
start = 1;
for i = 1:numThetas
	out = networkStructure(i + 1);
	in = networkStructure(i) + 1;
	cells = out * in;

	matrixCells{i} = reshape(nnParamVector(start:start + cells - 1), out, in);
	start += cells;
end

end
	