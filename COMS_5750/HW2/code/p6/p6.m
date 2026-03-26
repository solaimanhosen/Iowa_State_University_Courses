clear; clc; close all;

% --- 2) Process each character (braille -> white, then stamp english -> black) ---
debug = false;          % set false to reduce figures
th    = 0.5;
pad   = 3;

% --- Read input ---
color_img = imread('./../../images/p6/in/2.jpg');
figure; imshow(color_img); title('Original');

% --- 1) Binarize + invert (same idea as your code) ---
bi = binarizeInvert(color_img, 0.5);
figure; imshow(bi); title('Inverted binary');

color_img = processChar(color_img, bi, ...
    './../../braille_cutouts/q.jpg', './../../english_cutouts/q.png', ...
    'Q', th, pad, debug);

color_img = processChar(color_img, bi, ...
    './../../braille_cutouts/w.jpg', './../../english_cutouts/w.jpg', ...
    'W', th, pad, debug);

color_img = processChar(color_img, bi, ...
    './../../braille_cutouts/y.jpg', './../../english_cutouts/y.jpg', ...
    'Y', th, pad, debug);

figure; imshow(color_img); title('Final result');

% --- Save ---
imwrite(color_img, './../../images/p6/out/2.jpg');


function bi = binarizeInvert(color_img, thresh)
    % Same behavior style as your original: im2bw then invert
    b  = im2bw(color_img, thresh);
    bi = ~b;  % dots -> 1
end

function strelMask = loadStrelFromImage(path, thresh)
    se = imread(path);
    strelMask = binarizeInvert(se, thresh);
end

function [positions, pixelMask] = detectPositionsAndMask(bi, strelMask, pad)
    % Erode to detect anchor positions
    positions = imerode(bi, strelMask);

    % Slightly dilate the strel then dilate positions to build pixel mask
    strelMask2 = imdilate(strelMask, strel('square', pad));
    pixelMask  = imdilate(positions, strelMask2);

    positions = positions ~= 0;
    pixelMask = pixelMask ~= 0;
end

function imgOut = paintMask(imgIn, mask, rgb)
    % Paint pixels under mask with rgb = [R G B]
    mask = mask ~= 0;
    imgOut = imgIn;

    R = imgOut(:,:,1);  G = imgOut(:,:,2);  B = imgOut(:,:,3);
    R(mask) = rgb(1);
    G(mask) = rgb(2);
    B(mask) = rgb(3);
    imgOut(:,:,1) = R;  imgOut(:,:,2) = G;  imgOut(:,:,3) = B;
end

function imgOut = processChar(imgIn, bi, brailleCutoutPath, englishCutoutPath, label, thresh, pad, debug)
    % 1) load braille strel
    brailleStrel = loadStrelFromImage(brailleCutoutPath, thresh);
    if debug
        figure; imshow(brailleStrel); title([label ' Structural Element']);
    end

    % 2) detect braille positions + pixel mask
    [pos, brailleMask] = detectPositionsAndMask(bi, brailleStrel, pad);
    fprintf('Detected %s positions: %d\n', label, sum(pos(:)));

    if debug
        figure; imshow(brailleMask); title([label ' character pixel mask (braille)']);
    end

    % 3) remove braille by painting it white
    imgOut = paintMask(imgIn, brailleMask, [255 255 255]);

    % 4) stamp english glyph at detected positions (your method: dilate positions)
    engStrel = loadStrelFromImage(englishCutoutPath, thresh);
    if debug
        figure; imshow(engStrel); title([label ' English cutout strel']);
    end

    engMask = imdilate(pos, engStrel) ~= 0;

    if debug
        figure; imshow(engMask); title([label ' pixel mask (english stamp)']);
    end

    % 5) paint english stamp black
    imgOut = paintMask(imgOut, engMask, [0 0 0]);

    if debug
        figure; imshow(imgOut); title([label ' applied']);
    end
end

