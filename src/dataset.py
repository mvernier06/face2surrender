import os
from PIL import Image
from torch.utils.data import Dataset, DataLoader



class CelebADataset(Dataset):
    def __init__(self, root_dir, annotations_file, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_filenames = os.listdir(root_dir)
        self.attributes = self.parse_attributes(annotations_file)

    def __len__(self):
        return len(self.image_filenames)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir, self.image_filenames[idx])
        image = Image.open(img_name)
        if self.transform:
            image = self.transform(image)

        # Get attributes for the current image and convert to tensor
        attr = torch.tensor(self.attributes[self.image_filenames[idx]], dtype=torch.float32)

        return image, attr

    def parse_attributes(self, annotations_file):
        attributes = {}
        with open(annotations_file, 'r') as f:
            lines = f.readlines()
            header = lines[1].strip().split()  # Skip header line
            for line in lines[2:]:
                parts = line.strip().split()
                filename = parts[0]
                attr = [int(x) for x in parts[1:]]
                attributes[filename] = attr
        return attributes