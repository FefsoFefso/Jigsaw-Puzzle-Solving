import Image
import Genetic

if __name__ == '__main__':
    input_picture = int(input('Print image number (1200 - 1799): '))
    img = Image.PuzzlePicture(512, 64, 'data_train/64/' + str(input_picture) + '.png')
    img.show_image()
    img.cut_picture()
    metric = img.get_metric_matching_info()
    genetic = Genetic.Genetic(64, 8, metric, 'images_parts/')

    polulation = genetic.init_population()
    genetic.do_genetic(polulation)
    img.debug(input_picture)
