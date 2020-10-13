# Decision Maker - ask a user is preference for each combination of items given
#
import tkinter as tk
import tkinter.ttk as ttk
from intounknown_lib.tk_gui import EnhancedButton, EnhancedLabel, EnhancedEntry

from random import shuffle
from pprint import pprint


def generation_combinations(items):
    ''' Generate combinations for items using network formula n*((n-1)/2) '''
    combinations = []

    # Generate unique combinations
    # n * ((n-1)/2) = unique combinations
    for i in range(0, len(items)):
        for j in range(i+1, len(items)):
            # if a item matches itself, skip it
            if i == j:
                continue

            tmp = [i, j]                # create pairing
            shuffle(tmp)                # shuffle of the order isn't always the same
            combinations.append(tmp)    # add to combinations

    shuffle(combinations)       # randomize combinations

    return combinations



class QuestionTracker:
    '''
        Class generates combinations of items to compare
        A question is requested and answers can be given through
            the answer methods
    '''
    ANSWER_YES = 1
    ANSWER_NO = 2
    ANSWER_MAYBE = 0

    def __init__(self, items=None, question=None):
        combinations = generation_combinations(items)       # create combinations from items
        self.items = items                  # the items we are comparing
        self.question = question            # question template (in "%s" format)
        self.combinations = combinations    # combinations we are iterating over
        self.current_combination = None     # this is the current combination we need a answer for
        self.combination_length = len(combinations)     # store combination length for progress tracking

        self.scores = {}                    # keep track of scores

    def get_current_progress(self):
        ''' get the amount of questions remaining to be ask and the total amount of questions '''
        remaining_items = len(self.combinations)      # remain number of combinations
        total = self.combination_length     # total number of combinations before mutation
        count = total - remaining_items     # get progress to toward total

        return {
            'offset': count,
            'total': total,
        }

    def _lookup_item_name(self, obj_id):
        ''' get the name of an item by it's index '''
        return self.items.get(obj_id, None)

    def _lookup_combination_item_names(self):
        ''' lookup the item names and return '''
        a, b = self.current_combination
        item_a = self.items[a]      # get name for A
        item_b = self.items[b]      # get name for B
        return item_a, item_b

    def get_question(self):
        ''' Returns a question or None if no more combinations left to create a question from '''

        # If combination is not loaded then pop one from list
        if self.current_combination is None:
            try:
                self.current_combination = self.combinations.pop()
            except IndexError:
                return None

        # Get the item names from the combination
        item_a, item_b =  self._lookup_combination_item_names()

        question_txt = self.question % (item_a, item_b)
        return question_txt

    def _answer_question(self, response=None):
        ''' the response will be if item A preferred '''

        # If not more questions to be answered
        if self.current_combination == None:
            return

        a, b = self.current_combination
        # Item A is preferred
        if response == self.ANSWER_YES:
            if a not in self.scores:
                self.scores[a] = 0
            self.scores[a] += 1

        # Item B is preferred instead
        elif response == self.ANSWER_NO:
            if b not in self.scores:
                self.scores[b] = 0
            self.scores[b] += 1

        # If user can not decide
        elif response == self.ANSWER_MAYBE:
            if a not in self.scores:
                self.scores[a] = 0
            self.scores[a] += 0.5
            if b not in self.scores:
                self.scores[b] = 0
            self.scores[b] += 0.5

        # other forms of unknown input
        else:
            raise Exception('input ['+str(response)+'] is unknown')

        self.current_combination = None

    def answer_question_yes(self):
        self._answer_question(response=self.ANSWER_YES)

    def answer_question_no(self):
        self._answer_question(response=self.ANSWER_NO)

    def answer_question_maybe(self):
        self._answer_question(response=self.ANSWER_MAYBE)

    def get_scores(self):
        ''' Return the items and each items score in descending order
        :return:
                [{'id':1, 'name': ___, 'score' : 1},]
        '''

        result = []
        '''
            result = [
                {'id':1, 'name': ___, 'score' : 1},
            ]
        '''
        # Create a result set for each item and it's score
        for idx in range(0, len(self.items)):
            score = self.scores.get(idx, 0)     # an item's score by its index
            result.append({
                'id': idx,
                'name': self.items[idx],
                'score': score,
            })

        # sort items by score ascending
        result.sort(key=lambda a: a['score'])
        result.reverse()    # reverse order so items are descending by score
        return result

    def dump(self):
        ''' test function to display scores '''
        scores = self.get_scores()
        for obj in scores:
            print('%s - %s - %s ' % (obj['id'], obj['name'], obj['score']))

        pprint(self.current_combination)



class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.question_tracker = None

    def setup(self, question_tracker):
        self.question_tracker = question_tracker
        self.create_widgets()

    def create_widgets(self):
        self.title("Decision Maker")
        self.geometry("700x400")

        # Setup content area
        self.main_container = tk.Frame(self)
        content = ttk.LabelFrame(self.main_container, text="Decision")

        # Row 0
        self.progress_txt = EnhancedLabel(content, "Loading...")
        self.progress_txt.grid(row=0, column=0, columnspan=3, sticky=(tk.W + tk.E))

        # Row 1
        self.question_txt = EnhancedLabel(content, "Loading...")
        self.question_txt.grid(row=1, column=0, columnspan=3, sticky=(tk.W + tk.E))

        # Row 2
        EnhancedButton(content, "Choose A", command=self._click_item_a)\
            .grid(row=2, column=0, sticky=(tk.W + tk.N))
        EnhancedButton(content, "Choose B", command=self._click_item_b)\
            .grid(row=2, column=1, sticky=(tk.W + tk.N))
        EnhancedButton(content, "Unsure", command=self._click_item_maybe)\
            .grid(row=2, column=2, sticky=(tk.W + tk.N))


        result_frame = ttk.LabelFrame(self.main_container, text="Result:")
        # Row 0
        self.result_txt = EnhancedLabel(result_frame, "not result yet")
        self.result_txt.grid(row=0, column=0, rowspan=3, columnspan=3, sticky=(tk.W + tk.E + tk.N + tk.S))

        result_frame.grid(row=1, column=0, sticky=tk.W)

        content.grid(row=0, column=0, sticky=tk.W)
        self.main_container.grid(row=0, column=0, sticky=(tk.N, tk.W))

        self._queue_up_next_question()

    def _get_scores_formatted(self):
        result = []
        scores = self.question_tracker.get_scores()
        for obj in scores:
            obj_id = obj['id']
            name = obj['name']
            score = obj['score']

            txt = '%s - %s' % (score, name)
            result.append(txt)

        tmp = "\n".join(result)
        return tmp


    def _queue_up_next_question(self):
        next_question = self.question_tracker.get_question()
        if next_question == None:
            next_question = 'Completed'
            self.question_tracker.dump()

            txt = self._get_scores_formatted()
            self.result_txt.set(txt)

        self.question_txt.set(next_question)
        process_status = self.question_tracker.get_current_progress()

        offset = process_status['offset']
        total = process_status['total']

        process_txt = "Progress: %s of %s questions completed"
        msg = process_txt % (offset, total)

        self.progress_txt.set(msg)



    def _click_item_a(self):
        self.question_tracker.answer_question_yes()
        self._queue_up_next_question()

    def _click_item_b(self):
        self.question_tracker.answer_question_no()
        self._queue_up_next_question()

    def _click_item_maybe(self):
        self.question_tracker.answer_question_maybe()
        self._queue_up_next_question()


if __name__ == '__main__':
    #items = ['orange', 'yellow', 'blue']
    items = ['orange', 'yellow', 'blue', 'green', 'purple']
    question = 'Which do you prefer [%s] or [%s]? '

    q = QuestionTracker(items=items, question=question)
    app = Application()
    app.setup(q)        # pass question tracker to Application to be used
    app.mainloop()
    quit()

