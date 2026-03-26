%% Erode Circles Image

a=imread('circles.jpg');
imshow (a)

b=im2bw(a, 0.5);
imshow(b)

bi = ~b;
imshow(bi)


se=strel('square',3);

e1=imerode(bi, se);
figure; imshow(e1);

e2=imerode(e1, se);
figure; imshow(e2);

e3=imerode(e2, se);
figure; imshow(e3);


%%%%%%%%%%%%%%%%%%%%%
%   Erode Lines
%%%%%%%%%%%%%%%%%%%%%

l=imread('lines.jpg');
imshow(l)

b=im2bw(l, 0.5);
imshow(b)

bi= ~b;
imshow(bi)

% Get the Horizontal Lines only
se_h=strel('line', 40,0); %len, angle
h= imerode(bi, se_h);
imshow(h)

% Get the Vertical Lines only
se_v=strel('line', 40,90); % len, angle
v= imerode(bi, se_v);
imshow(v)


%%%%%%%%%%%%%%%%%%%%%
%   One 
%%%%%%%%%%%%%%%%%%%%%

o=imread('one.jpg');
imshow(o)

b=im2bw(o, 0.5);
imshow(b)

bi= ~b;
imshow(bi)

% This leaves a small part behind
se_h=strel('line', 40,0); %len, angle
h= imerode(bi, se_h);
imshow(h)

% Now Get all of it
se_h=strel('line', 50,0); %len, angle
h= imerode(bi, se_h);
imshow(h)


% We must dilate to get the stuff that was lost
h2=imdilate(h, se_h);
figure; imshow(h2)


% now get the stem of the 1
stem=xor(bi, h2);
figure; imshow(stem)


%extract only the stem
se_v=strel('line', 40,90); % len, angle
v_stem= imerode(stem, se_v);
imshow(v_stem)

% Get all of the vertical stem
v_stem= imdilate(v_stem, se_v);
imshow(v_stem)


%%##
%%##  Now Get the horizontal stem
%%##

se_h=strel('line', 20,0); % len, angle
h_stem= imerode(stem, se_h);
imshow(h_stem)

% Get all of the horizontal stem
h_stem= imdilate(h_stem, se_h);
imshow(h_stem)



%% NOW RECONSTRUCT THE STEM
rr  = or(h_stem, v_stem);
imshow(rr)

rrr = or(rr, h2);
imshow(rrr)








%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Connected Components

[L, num]=bwlabel(h_stem);
imshow(L)
imagesc(L)

%% Get Area
AA = regionprops(L,'Area'); 
AA(1).Area
AA(2).Area
AA(3).Area


% For 8 connected components
[L, num]=bwlabel(h_stem, 8);

% Display it with color
imshow(label2rgb(L))
 

%% Delete stuff
res=find(L==1)

L(res)=0;
imshow(L)


%%%%%%%%%%%%%%%
% Centroid

CC = regionprops(L,'Centroid');
 
for i=1:num
  CC(i).Centroid
end


plot(CC(3).Centroid(1), CC(3).Centroid(2), 'r.')