clear; clc; close all;

a = imread('../../images/p2/in/1.jpg');
% a = imread('../../images/p2/in/2.jpg');
figure; imshow (a);

b = im2bw(a, 0.5);
bi = ~b;
figure; imshow(bi);

se = strel('square', 3);

d1 = imdilate(bi, se);
figure; imshow(d1);

d2 = imdilate(d1, se);
d3 = imdilate(d2, se);
d4 = imdilate(d3, se);

figure; imshow(d4);

d5 = imdilate(d4, se);
d6 = imdilate(d5, se);
figure; imshow(d6);

zeroRows = all(d6 == 0, 2);
d = diff([false; zeroRows; false]);
starts = find(d == 1);
ends   = find(d == -1) - 1;
rows = floor((starts + ends)/2);

if ~isempty(rows)
    if starts(1) == 1
        rows(1) = ends(1);              % last zero row at the top block
    end
    if ends(end) == numel(zeroRows)
        rows(end) = starts(end);        % first zero row at the bottom block
    end
end

zeroCols = all(d6 == 0, 1);
d = diff([false, zeroCols, false]);
starts = find(d == 1);
ends   = find(d == -1) - 1;
cols = floor((starts + ends)/2);

if ~isempty(cols)
    if starts(1) == 1
        cols(1) = ends(1);              % last zero row at the top block
    end
    if ends(end) == numel(zeroCols)
        cols(end) = starts(end);        % first zero row at the bottom block
    end
end

output_img = a;
for i = 1:length(rows)
    y = round(rows(i));
    output_img = insertShape(output_img, 'Line', ...
        [1, y, size(output_img, 2), y], ...
        'Color', [255, 0, 0], 'LineWidth', 2);
end

for i = 1:length(cols)
    x = round(cols(i));
    output_img = insertShape(output_img, 'Line', ...
        [x, 1, x, size(output_img, 1)], ...
        'Color', [255, 0, 0], 'LineWidth', 2);
end

figure; imshow(output_img);

imwrite(output_img, '../../images/p2/out/1.jpg');
% imwrite(output_img, '../../images/p2/out/2.jpg');
