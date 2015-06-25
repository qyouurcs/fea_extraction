function resize_img(img_dir, save_dir, n)
    fns = dir(img_dir);
    if ~isdir(save_dir)
        mkdir(save_dir);
    end
    for i = 1:numel(fns)
        fn = fns(i);
        if fn.isdir
            continue;
        end
        full_fn = fullfile(img_dir, fn.name);
        im = imread(full_fn);
        if ndims(im) == 2
            im = cat(3, im, im, im);
        end
        im = imresize(im, [n n]);
        imwrite(im, fullfile(save_dir, fn.name));
        
    end
end
