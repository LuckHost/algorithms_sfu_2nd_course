import threading
import argparse
from PIL import Image, ImageDraw

class QuadtreeNode:
    """Node for Quadtree that holds a subsection of an image and
        information about that section"""

    def __init__(self, img, box, depth):
        self.box = box  # (left, top, right, bottom)
        self.depth = depth
        self.children = None  # tl, tr, bl, br
        self.leaf = False

        # Gets the nodes average color
        image = img.crop(box)
        self.width, self.height = image.size  # (width, height)
        hist = image.histogram()
        self.color, self.error = self.color_from_histogram(hist)  # (r, g, b), error

    def weighted_average(self, hist):
        """Returns the weighted color average and error from a hisogram of pixles"""
        total = sum(hist)
        value, error = 0, 0
        if total > 0:
            value = sum(i * j for i, j in enumerate(hist)) / total
            error = sum(j * (value - i) ** 2 for i, j in enumerate(hist)) / total
            error = error ** 0.5
        return value, error

    def color_from_histogram(self, hist):
        """Returns the average rgb color from a given histogram of pixel color counts"""
        r, re = self.weighted_average(hist[:256])
        g, ge = self.weighted_average(hist[256:512])
        b, be = self.weighted_average(hist[512:768])
        e = re * 0.2989 + ge * 0.5870 + be * 0.1140
        return (int(r), int(g), int(b)), e

    def split(self, img):
        '''
        Divide image into 4 ports
        :param img: image
        :return: None
        '''
        l, t, r, b = self.box
        lr = l + (r - l) / 2
        tb = t + (b - t) / 2
        tl = QuadtreeNode(img, (l, t, lr, tb), self.depth+1)
        tr = QuadtreeNode(img, (lr, t, r, tb), self.depth+1)
        bl = QuadtreeNode(img, (l, tb, lr, b), self.depth+1)
        br = QuadtreeNode(img, (lr, tb, r, b), self.depth+1)
        self.children = [tl, tr, bl, br]

class Tree:
    """Tree that has nodes with at most four child nodes that hold
        sections of an image where there at most n leaf nodes where
        n is the number of pixels in the image
    """

    def __init__(self, image):
        self.root = QuadtreeNode(image, image.getbbox(), 0)
        self.width, self.height = image.size
        self.max_depth = 7

        self._build_tree(image, self.root)

    def _build_tree(self, image, node):
        """Recursively adds nodes untill max_depth is reached or error is less than 12"""
        if (node.depth >= self.max_depth) or (node.error <= 12):
            node.leaf = True
            return
        node.split(image)

        if node.depth == 0:
            threads = []
            for child in node.children:
                thread = threading.Thread(target=self._build_tree, args=(image, child))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

        else:
            for child in node.children:
                self._build_tree(image, child)

    def get_leaf_nodes(self, depth):
        """Gets all the nodes on a given depth/level"""
        def get_leaf_nodes_recusion(tree, node, depth, func):
            """Recusivley gets leaf nodes based on whether a node is a leaf or the given depth is reached"""
            if node.leaf is True or node.depth == depth:
                func(node)
            elif node.children is not None:
                for child in node.children:
                    get_leaf_nodes_recusion(tree, child, depth, func)

        if depth > self.max_depth:
            depth = self.max_depth

        leaf_nodes = []
        get_leaf_nodes_recusion(self, self.root, depth, leaf_nodes.append)
        return leaf_nodes

    def make_img(self, depth, lines):
        """Creates a Pillow image object from a given level/depth of the tree"""
        image = Image.new('RGB', (int(self.width),
                                  int(self.height)))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, self.width,
                        self.height))

        leaf_nodes = self.get_leaf_nodes(depth)
        for node in leaf_nodes:
            l, t, r, b = node.box
            box = (l, t, r - 1, b - 1)
            if lines:
                draw.rectangle(box, node.color, outline=(0, 0, 0))
            else:
                draw.rectangle(box, node.color)
        return image


if __name__ == '__main__':
    'MAIN FUNCTION'
    parser = argparse.ArgumentParser(description="Make quadtree image")
    parser.add_argument("image_path", type=str, help="Path to the image")
    parser.add_argument('-d', "--depth", type=int, default=2, help="Depth in tree")
    parser.add_argument('-l', "--lines", action="store_true", help="Show lines in image")
    parser.add_argument('-m', "--max_depth", action="store_true", help="show maximum depth of an image")
    parser.add_argument('-glove', "--gif_glove", action="store_true", help="create gif")

    args = parser.parse_args()

    img = Image.open(args.image_path).convert('RGB')
    qtree = Tree(img)
    depth = args.depth
    output_image = qtree.make_img(depth, lines=args.lines)
    output_image.save("compressed_img.jpg")
    
    if args.gif_glove:
      frames = []
      for i in range(qtree.max_depth):
        output_image = qtree.make_img(i, lines=args.lines)
        frames.append(output_image)
      frames[0].save(
        'compress_gif.gif',
        save_all=True,
        append_images=frames[1:],  # Срез который игнорирует первый кадр.
        optimize=True,
        duration=800,
        loop=0
      )
        
      

    if args.max_depth:
        print(f'max depth of an image is {qtree.max_depth}')