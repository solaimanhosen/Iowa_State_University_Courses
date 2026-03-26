
clear; clc; close all;

a = imread('../../images/p9/in/1.jpg');
% a = imread('../../images/p9/in/2.jpg');
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

% height = rows(2) - rows(1); 
% width = cols(2) - cols(1); 
% fprintf("height: %d, width: %d\n", height, width); 

output_img = a;
% for i = 1:length(rows)
%     y = round(rows(i));
%     output_img = insertShape(output_img, 'Line', ...
%         [1, y, size(output_img, 2), y], ...
%         'Color', [255, 0, 0], 'LineWidth', 2);
% end
% 
% for i = 1:length(cols)
%     x = round(cols(i));
%     output_img = insertShape(output_img, 'Line', ...
%         [x, 1, x, size(output_img, 1)], ...
%         'Color', [255, 0, 0], 'LineWidth', 2);
% end
% 
% figure; imshow(output_img);

for i = 1:length(rows)-1
    for j = 1:length(cols)-1
        r1 = rows(i);
        r2 = rows(i+1) - 1;   % end just before next grid line
        c1 = cols(j);
        c2 = cols(j+1) - 1;

        % optional clamp to bounds
        r1 = max(1, r1); r2 = min(size(output_img,1), r2);
        c1 = max(1, c1); c2 = min(size(output_img,2), c2);

        % crop
        I = output_img(r1:r2+5, c1:c2+5, :);
        % I = binarizeInvert(I, 0.5);
        % figure; imshow(I);
        % sh = size(I);
        % fprintf('Size: %d x %d\n', sh(1), sh(2));

        letter = identifyLetter(I);
        fprintf("%s", letter);

        % mark point for visualization (don't permanently modify output_img unless you want accumulation)
        % vis = insertShape(output_img, 'Circle', [c1, r1, 2], ...
        %                   'Color', [0 255 0], 'LineWidth', 2);
        % 
        % figure; imshow(vis); title('Marked');
        % figure; imshow(I);   title('Cropped');
    end
end

% ch = 'c';
% label = upper(ch);
% 
% braillePath = fullfile('..','..','braille_cutouts', [ch '.jpg']);
% strelMask = loadStrelFromImage(braillePath, 0.5);

% sh = size(strelMask);
% fprintf('Size: %d x %d\n', sh(1), sh(2));

function letter = identifyLetter(color_img)
    letter = '-1';

    bi = binarizeInvert(color_img, 0.5);
    figure; imshow(bi);

    letters = ['y','z','w','x','v','u','q','p','r','l','t','s','n','m','o','k','g','d','f','h','j','b','c','e','i','a'];

    for k = 1:numel(letters)
        ch = letters(k);
        label = upper(ch);

        braillePath = fullfile('..','..','braille_cutouts', [ch '.jpg']);

        if ~isfile(braillePath)
            fprintf('Skipping %s (missing file): %s\n', label, braillePath);
            continue;
        end

        strelMask = loadStrelFromImage(braillePath, 0.5);

        positions = imerode(bi, strelMask);

        if any(positions(:))
            letter = ch;
            return;
        end
    end
end

function bi = binarizeInvert(color_img, thresh)
    % Same behavior style as your original: im2bw then invert
    b  = im2bw(color_img, thresh);
    bi = ~b;  % dots -> 1
end

function strelMask = loadStrelFromImage(path, thresh)
    se = imread(path);
    strelMask = binarizeInvert(se, thresh);
end

% x = 1;
% y = 2;
% 
% px = rows(x);
% py = cols(y);
% 
% output_img = a;
% 
% R = output_img(:, :, 1);
% G = output_img(:, :, 2);
% B = output_img(:, :, 3);
% 
% % Adjust the color channels based on the marked point
% for i = 1:width
%     for j = 1:height
%         R(px + j - 1, py + i - 1) = 255;   % Set the red channel to minimum
%         G(px + j - 1, py + i - 1) = 255; % Set the green channel to maximum
%         B(px + j - 1, py + i - 1) = 255;   % Set the blue channel to minimum
%     end
% end
% 
% output_img1 = cat(3, R, G, B);
% 
% % start fully white
% R = uint8(255*ones(size(output_img,1), size(output_img,2), 'like', output_img));
% G = R; 
% B = R;
% 
% for i = 1:width
%     for j = 1:height
%         R(px + j - 1, py + i - 1) = output_img(px + j - 1, py + i - 1, 1);
%         G(px + j - 1, py + i - 1) = output_img(px + j - 1, py + i - 1, 2);
%         B(px + j - 1, py + i - 1) = output_img(px + j - 1, py + i - 1, 3);
%     end
% end
% 
% output_img2 = cat(3, R, G, B);

% Mark the specific point (px, py) on the output image
% output_img1 = insertShape(output_img1, 'Circle', [py, px, 5], 'Color', [0, 255, 0], 'LineWidth', 2);
% 
% 
% for i = 1:length(rows)
%     y = round(rows(i));
%     output_img1 = insertShape(output_img1, 'Line', ...
%         [1, y, size(output_img1, 2), y], ...
%         'Color', [255, 0, 0], 'LineWidth', 2);
% end
% 
% for i = 1:length(cols)
%     x = round(cols(i));
%     output_img1 = insertShape(output_img1, 'Line', ...
%         [x, 1, x, size(output_img1, 1)], ...
%         'Color', [255, 0, 0], 'LineWidth', 2);
% end
% 
% figure; imshow(output_img1);
% 
% % Mark the specific point (px, py) on the output image
% output_img1 = insertShape(output_img2, 'Circle', [py, px, 5], 'Color', [0, 255, 0], 'LineWidth', 2);
% 
% 
% for i = 1:length(rows)
%     y = round(rows(i));
%     output_img1 = insertShape(output_img1, 'Line', ...
%         [1, y, size(output_img1, 2), y], ...
%         'Color', [255, 0, 0], 'LineWidth', 2);
% end
% 
% for i = 1:length(cols)
%     x = round(cols(i));
%     output_img1 = insertShape(output_img1, 'Line', ...
%         [x, 1, x, size(output_img1, 1)], ...
%         'Color', [255, 0, 0], 'LineWidth', 2);
% end
% 
% figure; imshow(output_img1);

% imwrite(output_img2, '../../images/p3/out/1a.jpg');
% imwrite(output_img1, '../../images/p3/out/1b.jpg');
% imwrite(output_img2, '../../images/p3/out/2a.jpg');
% imwrite(output_img1, '../../images/p3/out/2b.jpg');
