%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Dilation example from last lecture
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Dilation original example
A=zeros(6,5)
A(2:5, 3)=1
se=[1 0 1]
imdilate (A, se)


%Dilation, new example
A=zeros(6,5)
A(2:5, 3)=1
se=[1 0 1]
imdilate (A, se)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Histograms for skull image
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


a=imread('skull.jpg');
imshow(a)

b=rgb2gray(a);
imhist(b, 20)
imhist(b, 10)


%Another way to do it
[count, X] = imhist(b, 20);
count
X 

%% Histogram equalization
J=histeq(b, 20); % with 20 bins
mshow(J)
figure; imshow(b)




%%%%%%%%%%%%%%%%%%%%
%%   Adding Noise
%%%%%%%%%%%%%%%%%%%%

% How to get help
more on
help imnoise

cy= imread('cy.jpg');
cy = rgb2gray(cy);
imshow (cy)
SP = imnoise(cy,'salt & pepper', 0.05);
figure; imshow(SP)

G= imnoise(cy, 'gaussian', 0, 0.05);
figure; imshow(G)


%%%%%%%%%%%%%%%%%%%%
%%   Filtering
%%%%%%%%%%%%%%%%%%%%


SP = imnoise(cy,'salt & pepper', 0.05);
figure; imshow(SP)


%% Mean Filter
H=fspecial('average')

H=fspecial('average', 5)

H=fspecial('average', 3)
M= imfilter (SP, H);
figure; imshow(M)



%% Median Filter


K = medfilt2(SP);
figure; imshow(K)
	

%% Gaussian Filter

H=fspecial('gaussian', 7, 3)

imshow(G)
H=fspecial('gaussian', 3, sqrt(2))
F= imfilter (G, H);
figure; imshow(F)

H7 = [ 1, 1, 2,  2, 2, 1, 1;
       1, 2, 2,  4, 2, 2, 1;
       2, 2, 4,  8, 4, 2, 2;
       2, 4, 8, 16, 8, 4, 2;
       2, 2, 4,  8, 4, 2, 2;
       1, 2, 2,  4, 2, 2, 1;
       1, 1, 2,  2, 2, 1, 1 ]

% sum is 140
sum(sum(H7))

imfilter (ones(14), H7./140)

imfilter (ones(14), H7./140, 1) % pad it with 1's


H7b = [  1,  4,  7, 10,  7,  4,  1;
         4, 12, 26, 33, 26, 12,  4;
         7, 26, 55, 71, 55, 26,  7;
        10, 33, 71, 91, 71, 33, 10;
         7, 26, 55, 71, 55, 26,  7;
         4, 12, 26, 33, 26, 12,  4;
         1,  4,  7, 10,  7,  4,  1 ]


% sum is 1115
sum(sum(H7b))


imfilter (ones(14), H7b./1115)



%%%%%%%%%%%%%%%%%%%%
%%   Pyramids
%%%%%%%%%%%%%%%%%%%%
cy = imread('cy.jpg');
imshow(cy)

P1= impyramid(cy, 'reduce');
figure; imshow(P1)

P2= impyramid(P1, 'reduce');
P3= impyramid(P2, 'reduce');

figure; imshow(P2)
figure; imshow(P3)


%% Compare that with just deleting every even row and column
cc = cy(1:2:end, 1:2:end, :);
figure; imshow(cc)

diff = abs(P1-cc);
figure; imshow(diff)
