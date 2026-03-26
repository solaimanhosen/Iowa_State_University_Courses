clear; clc; close all;

% -------------------- CONFIG --------------------
imgPath    = fullfile('..','..','images','p9','in','2.jpg');   % change to 2.jpg if needed
th         = 0.5;       % binarization threshold
dilateIter = 6;         % how many dilations to build grid mask
seSize     = 3;         % square strel size for dilation
margin     = 5;         % extra pixels added to r2/c2 crop (clamped safely)
debug      = false;     % set true to visualize intermediate crops/masks

brailleDir = fullfile('..','..','braille_cutouts');


letters = ['e'];

% --- Read image ---
a = imread(imgPath);
figure; imshow(a); title('Original');

% --- Binarize + invert (dots -> 1) ---
bi = binarizeInvert(a, th);
figure; imshow(bi); title('Inverted binary (dots=1)');

se = strel('square', seSize);

for k = 1:numel(letters)
    ch = letters(k);
    braillePath = fullfile(brailleDir, [ch '.jpg']);

    if ~isfile(braillePath)
        continue;
    end

    strelMask = loadStrelFromImage(braillePath, th);
    strelMask = imerode(strelMask, se);

    figure; imshow(strelMask);

    positions = imerode(bi, strelMask);
    figure; imshow(positions);
end

%% FUNCTIONS %%

function bi = binarizeInvert(color_img, thresh)
    % Compatible with your usage (im2bw supports RGB by converting to gray internally in many MATLAB versions)
    b  = im2bw(color_img, thresh);
    bi = ~b;  % dots -> 1
end

function strelMask = loadStrelFromImage(path, thresh)
    se = imread(path);
    strelMask = binarizeInvert(se, thresh);
end