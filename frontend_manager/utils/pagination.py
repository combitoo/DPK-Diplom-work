async def get_pagintaion_page(limit: int = 3, offset: int = 0, pages_amount: int = 0, type_for: str = ""):
    if offset == 0 and pages_amount == 0:
        # Если первая страница и больше нет страниц
        prev_button = 0
        next_button = 0
    elif offset == 0 and pages_amount > 0:
        # Если первая страница и есть страницы
        prev_button = 0
        next_button = offset + 1
    elif offset + 1 >= pages_amount:
        # Если последняя страница
        prev_button = offset - 1
        next_button = offset
    else:
        # Любая страница посередине
        prev_button = offset - 1
        next_button = offset + 1

    pagination_html = f"""
    <nav aria-label="Page navigation example w-full" class="flex">
        <ul class="flex items-center -space-x-px h-10 text-base">
            <li>
                <a href="{type_for}/?offset={ prev_button }" class="flex items-center justify-center px-4 h-10 ms-0 leading-tight text-gray-500 bg-white border border-e-0 border-gray-300 rounded-s-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                    <span class="sr-only">Назад</span>
                    <svg class="w-3 h-3 rtl:rotate-180" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 6 10">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 1 1 5l4 4"/>
                    </svg>
                </a>
            </li>
            <li>
                <a href="{type_for}/?offset={ offset }" aria-current="page" class="z-10 flex items-center justify-center px-4 h-10 leading-tight text-blue-600 border border-blue-300 bg-blue-50 hover:bg-blue-100 hover:text-blue-700 dark:border-gray-700 dark:bg-gray-700 dark:text-white">{ offset + 1 }</a>
            </li>
            <li disabled='True'>
                <a href="{type_for}/?offset={ next_button }" class="flex items-center justify-center px-4 h-10 leading-tight text-gray-500 bg-white border border-gray-300 rounded-e-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                    <span class="sr-only">Далее</span>
                    <svg class="w-3 h-3 rtl:rotate-180" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 6 10">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 9 4-4-4-4"/>
                    </svg>
                </a>
            </li>
        </ul>
        <div class="flex items-center justify-center">
            <p class="text-gray-500 dark:text-gray-400 ml-3 text-center items-center">Всего { pages_amount } стр.</p>
        </div>
    </nav>
    """

    return pagination_html