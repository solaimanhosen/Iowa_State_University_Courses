clear; clc; close all;

a = imread('./../../images/p7/in/1.jpg');
% a = imread('./../../images/p7/in/2.jpg');
figure; imshow(a); title('Original');

%% -- 1. Binarize (replicate im2bw 0.5) --------------------------------------
b  = im2bw(a, 0.5);         % white background -> 1, dark dots -> 0
bi = ~b;                    % invert: dots -> 1 (foreground)
figure; imshow(bi); title('Inverted binary');

%% -- 2. Read Structural Elements
se = imread('./../../braille_cutouts/p.jpg');
se_bw = im2bw(se, 0.5);
p_strel = ~se_bw;

figure; imshow(p_strel); title('P Structural Element');

se = imread('./../../braille_cutouts/t.jpg');
se_bw = im2bw(se, 0.5);
t_strel = ~se_bw;
figure; imshow(t_strel); title('T Structural Element');

se = imread('./../../braille_cutouts/s.jpg');
se_bw = im2bw(se, 0.5);
s_strel = ~se_bw;

figure; imshow(s_strel); title('S Structural Element');

%% -- 3. Find P positions
p_positions = imerode(bi, p_strel);
fprintf('Detected S positions: %d\n', sum(p_positions(:)));

onlyP = imdilate(p_positions, p_strel);
figure; imshow(onlyP); title('S character pixel mask');

%% -- 3. Find T positions
t_positions = imerode(bi, t_strel);
fprintf('Detected S positions: %d\n', sum(p_positions(:)));

onlyT = imdilate(t_positions, t_strel);
figure; imshow(onlyT); title('T character pixel mask');

%% -- 4. Color P pixels WHITE in the original image --------------------------
color_img = a;
R = color_img(:,:,1);
G = color_img(:,:,2);
B = color_img(:,:,3);

pos    = find(onlyP == 1);
R(pos) = 255;
G(pos) = 255;
B(pos) = 255;

color_img(:,:,1) = R;
color_img(:,:,2) = G;
color_img(:,:,3) = B;

figure; imshow(color_img); title('P characters colored WHITE');

%% -- 4. Color T pixels WHITE in the original image --------------------------
R = color_img(:,:,1);
G = color_img(:,:,2);
B = color_img(:,:,3);

pos    = find(onlyT == 1);
R(pos) = 255;
G(pos) = 255;
B(pos) = 255;

color_img(:,:,1) = R;
color_img(:,:,2) = G;
color_img(:,:,3) = B;

figure; imshow(color_img); title('T characters colored WHITE');

%% -- 1. Binarize (replicate im2bw 0.5) --------------------------------------
b  = im2bw(color_img, 0.5);         % white background -> 1, dark dots -> 0
bi = ~b;                    % invert: dots -> 1 (foreground)
figure; imshow(bi); title('Inverted binary');

%% -- 3. Find S positions
s_positions = imerode(bi, s_strel);
fprintf('Detected S positions: %d\n', sum(s_positions(:)));

onlyS = imdilate(s_positions, s_strel);
figure; imshow(onlyS); title('S character pixel mask');

%% -- 4. Color S pixels GREEN in the original image --------------------------
color_img = a;
R = color_img(:,:,1);
G = color_img(:,:,2);
B = color_img(:,:,3);

pos    = find(onlyS == 1);
R(pos) = 0;
G(pos) = 200;
B(pos) = 0;

color_img(:,:,1) = R;
color_img(:,:,2) = G;
color_img(:,:,3) = B;

figure; imshow(color_img); title('S characters colored GREEN');

%% -- 5. Save result ---------------------------------------------------------
imwrite(color_img, './../../images/p7/out/1.jpg');
% imwrite(color_img, './../../images/p7/out/2.jpg');
