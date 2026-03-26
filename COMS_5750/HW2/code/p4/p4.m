clear; clc; close all;

a = imread('./../../images/p4/in/2.jpg');
% a = imread('./../../images/p4/in/2.jpg');
figure; imshow(a); title('Original');

%% -- 1. Binarize (replicate im2bw 0.9) --------------------------------------
b  = im2bw(a, 0.5);         % white background -> 1, dark dots -> 0
bi = ~b;                    % invert: dots -> 1 (foreground)
figure; imshow(bi); title('Inverted binary');

%% -- 2. Read Structural Element

se = imread('./../../braille_cutouts/q.jpg');
se_bw = im2bw(se, 0.5);
q_strel = ~se_bw;

figure; imshow(q_strel); title('Q Structural Element');

%% -- 3. Find Q positions
q_positions = imerode(bi, q_strel);
fprintf('Detected Q positions: %d\n', sum(q_positions(:)));

onlyQ = imdilate(q_positions, q_strel);
figure; imshow(onlyQ); title('Q character pixel mask');

%% -- 4. Color Q pixels GREEN in the original image --------------------------
color_img = a;
R = color_img(:,:,1);
G = color_img(:,:,2);
B = color_img(:,:,3);

pos    = find(onlyQ == 1);
R(pos) = 0;
G(pos) = 200;
B(pos) = 0;

color_img(:,:,1) = R;
color_img(:,:,2) = G;
color_img(:,:,3) = B;

figure; imshow(color_img); title('Q characters colored GREEN');

%% -- 8. Save result ---------------------------------------------------------
imwrite(color_img, './../../images/p4/out/2.jpg');
% imwrite(color_img, './../../images/p4/out/2.jpg');

